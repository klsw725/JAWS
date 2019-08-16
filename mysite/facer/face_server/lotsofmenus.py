import pymysql
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Images

engine = create_engine('mysql+pymysql://root:root@localhost/test')
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

print ("연결 성공 menu items!")

# print(os.path.dirname(os.path.realpath("pics/seungwoo.jpg")))
seungwoo = Images(name="seungwoo", location = "pics/seungwoo.jpg")

session.add(seungwoo)
session.commit()


print ("added menu items!")