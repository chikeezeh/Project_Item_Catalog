from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify
# import modules login functionality
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# create the CLIENT_ID from the Google JSON file.
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# create the flask app instant
app = Flask(__name__)

engine = create_engine('sqlite:///catalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a state token to preven request forgery
# Store it in the session for later validation


@app.route('/login')
def showLogin():
    state = ''.join(random.choice
                    (string.ascii_uppercase +
                     string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
# create gconnect function


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if a user exist in the database, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """
    'style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;'> """
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT -Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully logged out')
        return redirect(url_for('showCategory'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# create a user from the login information provided.
# the user is identified by email, hence using different oauth2 provider, but
# with the same email address would result in he same user

# helper functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
# end helper functions


@app.route('/category/JSON')
def showCategoryJSON():  # all category API
    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/category/<int:category_id>/item/JSON')
def showItemJSON(category_id):  # all item in a given category  API
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[item.serialize for item in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def oneItemJSON(category_id, item_id):  # API for one item from a category.
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(category=category, id=item_id).one()
    return jsonify(item=[item.serialize])


@app.route('/category/catalog/JSON')
def allCatalogJSON():
    items = session.query(Item).all()
    return jsonify(catalog=[item.serialize for item in items])


@app.route('/')
@app.route('/category/')
def showCategory():  # show all category
    # get the name of the categories in the category table
    categories = session.query(Category).all()
    # check if user is not logged in, then show default items.
    if 'username' not in login_session:
        items = session.query(Item).filter_by(user_id=1)

    else:
        # if the user is logged in, show the recent items they added.
        items = session.query(Item).filter_by(user_id=login_session['user_id'])
        # return the categories html page, and pass categories from the
        # database to the html page.
    # get the name of the user
    # if the user is not logged in return default user
    # else return the user
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    return render_template('categories.html', categories=categories,
                           recentItems=items, creator=creator)

# send the creator information to the header html file.


@app.route('/category/creator')
def itemCreator():
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    return render_template('header.html', creator=creator)


@app.route('/category/<int:category_id>/item')
def showItem(category_id):  # show the items that are in a particular category
    category = session.query(Category).filter_by(id=category_id).one()
    # check if user is not logged in, then show default items.
    if 'username' not in login_session:
        items = session.query(Item).filter_by(category_id=category_id,
                                              user_id=1).all()
    else:
        # if the user is logged in, show them their own item
        items = session.query(Item).filter_by(
            category_id=category_id,
            user_id=login_session['user_id']).all()
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    return render_template('items.html', items=items, category=category,
                           creator=creator)


@app.route('/category/<int:category_id>/item/<int:item_id>/description')
def descriptionItem(category_id, item_id):  # describe a selected item.
    itemToDescribe = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    return render_template('description.html', item=itemToDescribe,
                           creator=creator)


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
    # check if a user is logged in before they can make a new item.
    if 'username' not in login_session:
        return redirect('/login')
    # check if a post request is sent, then add the new item to the database.
    # after the new item is added render the category that the new item is in.
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        addItem = Item(name=request.form['title'],
                       category_id=category_id,
                       user_id=login_session['user_id'])
        addItem.description = request.form['description']
        session.add(addItem)
        flash('New Item %s was Successfully Added' % addItem.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('additem.html', category_id=category_id,
                               category=category, creator=creator)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    # select the item you want to delete
    itemToedit = session.query(Item).filter_by(id=item_id).one()
    # check if a user is logged in before they can make changes to an item.
    if 'username' not in login_session:
        return redirect('/login')
    # check if the user created this item.
    if itemToedit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    # check if you have a post request, then change the name, description, and
    # category_id to what the user supplies.
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    if request.method == 'POST':
        if request.form['title']:
            category_id = request.form['category']
            itemToedit.name = request.form['title']
            itemToedit.description = request.form['description']
            itemToedit.category_id = category_id
            session.add(itemToedit)
            flash('Item %s was Successfully Edited' % itemToedit.name)
            session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('edititem.html', item=itemToedit,
                               category_id=category_id, creator=creator)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['POST', 'GET'])
def deleteItem(category_id, item_id):
    # select the item to delete, then remove it from the database
    itemTodelete = session.query(Item).filter_by(id=item_id).one()
    # check if a user is logged in before they can delete an item.
    if 'username' not in login_session:
        return redirect('/login')
    if itemTodelete.user_id != login_session['user_id']:
        return "<script> function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.'); } </script > <body onload = 'myFunction()' >"  # noqa
    if 'username' not in login_session:
        creator = getUserInfo(1)
    else:
        creator = getUserInfo(login_session['user_id'])
    if request.method == 'POST':
        session.delete(itemTodelete)
        flash('Item %s was Successfully Deleted' % itemTodelete.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemTodelete,
                               category_id=category_id, creator=creator)


# run the server on localhost port 5000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
