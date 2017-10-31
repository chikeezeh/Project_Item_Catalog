#!/usr/bin/env python
# sqlalchemy is an ORM (Object-Relational Mapping) module that
# we will use to query our database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
# class for the users


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     email = Column(String(250), nullable=False)
#     picture = Column(String(250))

# class for the category


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)

# class for the item


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    course = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # user_id = Column(Integer, ForeignKey('user.id'))
    # user = relationship(User)


# create the database file
engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)
