import sys
import pymysql

from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine


# declarative_base() : Table 생성을 위한 부모 class인 Base 생성하는 함수
Base = declarative_base()


# class Restaurant(Base):
#     __tablename__ = 'restaurant'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#

class Images(Base):
    __tablename__ = 'api_images'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    image = Column(String(255), nullable=False)
    # data = Column(LargeBinary)
    # description = Column(String(250))
    # price = Column(String(8))
    # course = Column(String(250))
    # restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # restaurant = relationship(Restaurant)


##### insert at end of file #####

engine = create_engine('mysql+pymysql://root:root@localhost/test')

Base.metadata.create_all(engine)
