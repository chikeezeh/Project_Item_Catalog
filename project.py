from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import Flask, render_template, url_for, request, redirect

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

# show all categories


@app.route('/category/')
def showCategory():
    # get the name of the categories in the category table
    categories = session.query(Category).all()
    # return the categories html page, and pass categories from the
    # database to the html page.
    return render_template('categories.html', categories=categories)


@app.route('/category/<int:category_id>/item')
def showItem(category_id):  # show the items that are in a particular category
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category)


@app.route('/category/<int:category_id>/item/<int:item_id>/description')
def descriptionItem(category_id, item_id):
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
            session.commit()
        return redirect(url_for('showItem', category_id=category_id))
    else:
        return render_template('edititem.html', item=itemToedit,
                               category_id=category_id)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return render_template('deleteitem.html')


# run the server on localhost port 5000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
