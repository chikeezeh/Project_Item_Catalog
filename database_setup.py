#!/usr/bin/env python
# sqlalchemy is an ORM (Object-Relational Mapping) module that
# we will use to query our database
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# class for the category


class Category(Base):
    pass

# class for the item


class Item(Base):
    pass


# class for the users

class User(Base):
    pass
