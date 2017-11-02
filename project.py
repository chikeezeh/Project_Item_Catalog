from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
from flask import Flask, render_template, url_for

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
def showItem(category_id):
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items)


@app.route('/category/<int:category_id>/item/new')
def newItem(category_id):
    return render_template('additem.html')


@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def editItem(category_id, item_id):
    return render_template('edititem.html')


@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def deleteItem(category_id, item_id):
    return render_template('deleteitem.html')


# run the server on localhost port 5000
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
