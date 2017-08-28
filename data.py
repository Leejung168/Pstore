from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Host, Base, Passwd, User


from Crypto.Cipher import XOR
import base64

#engine = create_engine('sqlite:///keepass.db')
engine = create_engine('mysql://root:lambert@127.0.0.1:3306/keepass')
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

secret_key = '*XaDt(sfGd{6Qy+4q|.%0j;Fdm5?n!*~'
#Encrypt/Decrypt Password
def encrypt(plaintext, key=secret_key):
  cipher = XOR.new(key)
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(ciphertext, key=secret_key):
  cipher = XOR.new(key)
  return cipher.decrypt(base64.b64decode(ciphertext))

import random
import string
from random import choice
def generate_passwd(length):
    passwd_format = string.digits + string.ascii_letters
    passwd = []
    while (len(passwd) < length):
        passwd.append(choice(passwd_format))
    return ''.join(passwd)


for i in range(20):
    server3 = Host(servername="srv-{0}-db10{1}".format(generate_passwd(5), i), ip="10.10.1.1", port="40022", group="lz")
    session.add(server3)
    session.commit()

    passwd3 = Passwd(username="ncadmin",password=encrypt(generate_passwd(12)), host=server3)
    session.add(passwd3)
    session.commit()

    passwd4 = Passwd(username="root",password=encrypt(generate_passwd(12)),comment="PrivateIP:10.0.0.1", host=server3)
    session.add(passwd4)
    session.commit()

    passwd5 = Passwd(username="mysqlroot",password=encrypt(generate_passwd(12)),comment="PrivateIP:10.0.0.1", host=server3)
    session.add(passwd5)
    session.commit()

    passwd6 = Passwd(username="gpgkey",password=encrypt(generate_passwd(12)), comment="PrivateIP:10.0.0.1", host=server3)
    session.add(passwd6)
    session.commit()

#ser1 = User(name="lizheng")
#ser1.hash_password("lizheng")
#session.add(ser1)
#session.commit()
