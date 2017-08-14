import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    servername = Column(String(32))
    ip = Column(String(32))
    port = Column(String(16))
    group = Column(String(16))


class Passwd(Base):
    __tablename__ = 'passwds'
    id = Column(Integer, primary_key=True)
    username = Column(String(16))
    password = Column(String(64))
    comment = Column(String(250))
    passwds_id = Column(Integer, ForeignKey('hosts.id'))
    host = relationship(Host)


engine = create_engine('sqlite:///keepass.db')


Base.metadata.create_all(engine)
