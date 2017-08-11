from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Host, Base, Passwd

engine = create_engine('sqlite:///keepass.db')
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



server3 = Host(servername="srv-lz-lb1", ip="10.10.1.1", port="40022", group="lz")
session.add(server3)
session.commit()

passwd3 = Passwd(username="ncadmin",password="establishes", host=server3)
session.add(passwd3)
session.commit()

passwd4 = Passwd(username="root",password="secondone",comment="PrivateIP:10.0.0.1", host=server3)
session.add(passwd4)
session.commit()

passwd5 = Passwd(username="root",password="secondone",comment="PrivateIP:10.0.0.1", host=server3)
session.add(passwd5)
session.commit()

passwd6 = Passwd(username="gpgkey",password="instance", comment="PrivateIP:10.0.0.1", host=server3)
session.add(passwd6)
session.commit()
