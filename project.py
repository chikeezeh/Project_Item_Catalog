from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import Flask, render_template, url_for, request, redirect, flash
from flask import jsonify


# create the flask app instant
app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
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


@app.route('/category/')
def showCategory():  # show all category
    # get the name of the categories in the category table
    categories = session.query(Category).all()
    # obtain the most recent item added to the database.
    recentItems = []
    for i in range(1, 5):
        items = session.query(Item).filter_by(category_id=i).all()
        for item in items[-2:]:
            recentItems.append(item.name)
    # return the categories html page, and pass categories from the
    # database to the html page.
    return render_template('categories.html', categories=categories,
                           recentItems=recentItems)


@app.route('/category/<int:category_id>/item')
def showItem(category_id):  # show the items that are in a particular category
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/description')
def descriptionItem(category_id, item_id):  # describe a selected item.
    itemToDescribe = session.query(Item).filter_by(id=item_id).one()
    return render_template('description.html', item=itemToDescribe)


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def newItem(category_id):
    # check if a post request is sent, then add the new item to the database.
    # after the new item is added render the category that the new item is in.
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        addItem = Item(name=request.form['title'], category_id=category_id)
        addItem.description = request.form['description']
        session.add(addItem)
        flash('New Item %s was Successfully Added' % addItem.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('additem.html', category_id=category_id,
                               category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    # select the item you want to delete
    # check if you have a post request, then change the name, description, and
    # category_id to what the user supplies.
    itemToedit = session.query(Item).filter_by(id=item_id).one()
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
                               category_id=category_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
           methods=['POST', 'GET'])
def deleteItem(category_id, item_id):
    # select the item to delete, then remove it from the database
    # the return back to the category you started from
    itemTodelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemTodelete)
        flash('Item %s was Successfully Deleted' % itemTodelete.name)
        session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemTodelete,
                               category_id=category_id)


# run the server on localhost port 5000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
