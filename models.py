import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()

#Host info table
class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    servername = Column(String(32), nullable=False)
    ip = Column(String(32), nullable=False)
    port = Column(String(16), nullable=False)
    group = Column(String(16), nullable=False)

#Host username/password table
class Passwd(Base):
    __tablename__ = 'passwds'
    id = Column(Integer, primary_key=True)
    username = Column(String(16), nullable=False)
    password = Column(String(64), nullable=False)
    comment = Column(String(250))
    passwds_id = Column(Integer, ForeignKey('hosts.id'))
    host = relationship(Host)


#Flask-login user/password table
class User(Base,UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    password_hash = Column(String(250), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

#engine = create_engine('sqlite:///keepass.db')
engine = create_engine('mysql://root:lambert@127.0.0.1:3306/keepass')

Base.metadata.create_all(engine)
