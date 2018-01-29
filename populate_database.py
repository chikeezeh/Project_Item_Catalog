#!/usr/bin/env python
# python file to prepopulate the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
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

# create a dummy user
User1 = User(name="John Doe", email="john.doe@mail.com", picture="http://via.placeholder.com/400x400")  # noqa
session.add(User1)
session.commit()

# Make the categories
# category1 items
category1 = Category(user_id=1, name="Soccer")
session.add(category1)
session.commit()

# category2 items
category2 = Category(user_id=1, name="Snowboarding")
session.add(category2)
session.commit()

# category3 items
category3 = Category(user_id=1, name="Frisbee")
session.add(category3)
session.commit()

# category4 items
category4 = Category(user_id=1, name="Baseball")
session.add(category4)
session.commit()

# add items to each category
# category1 item1
item1 = Item(user_id=1, name="Soccer Cleats",
             description="Footwear for playing soccer", category=category1)
session.add(item1)
session.commit()
# category1 item2
item2 = Item(user_id=1, name="Soccer Balls",
             description="Balls for playing soccer", category=category1)
session.add(item2)
session.commit()

# category2 item1
item1 = Item(user_id=1, name="Snowboard", description="A board for sking",
             category=category2)
session.add(item1)
session.commit()
# category2 item2
item2 = Item(user_id=1, name="Gloves", description="To Keep Warm",
             category=category2)
session.add(item2)
session.commit()

# category3 item1
item1 = Item(user_id=1, name="Frisbee", description="Plate that is thrown",
             category=category3)
session.add(item1)
session.commit()
# category3 item2
item2 = Item(user_id=1, name="Jersey",
             description="Cloth for playing Frisbee", category=category3)
session.add(item2)
session.commit()

# category4 item1
item1 = Item(user_id=1, name="Bat",
             description="Used to hit the ball in baseball",
             category=category4)
session.add(item1)
session.commit()
# category4 item2
item2 = Item(user_id=1, name="Baseballs",
             description="Balls for playing Baseball", category=category4)
session.add(item2)
session.commit()

print "added all catalog items"
