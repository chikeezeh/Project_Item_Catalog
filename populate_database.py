#!/usr/bin/env python
# python file to prepopulate the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item

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

# Make the categories
# category1 items
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

# category2 items
category2 = Category(name="Snowboarding")
session.add(category2)
session.commit()

# category3 items
category3 = Category(name="Frisbee")
session.add(category3)
session.commit()

# category4 items
category4 = Category(name="Baseball")
session.add(category4)
session.commit()

# add items to each category
# category1 item1
item1 = Item(name="Soccer Cleats", description="Footwear for playing soccer",
             category=category1)
session.add(item1)
session.commit()

# category2 item1
item1 = Item(name="Snowboard", description="A board for sking",
             category=category2)
session.add(item1)
session.commit()

# category3 item1
item1 = Item(name="Frisbee", description="Plate that is thrown",
             category=category3)
session.add(item1)
session.commit()

# category4 item1
item1 = Item(name="Bat", description="Used to hit the ball in baseball",
             category=category4)
session.add(item1)
session.commit()

print "added all catalog items"
