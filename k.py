from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Host, Base, Passwd
import xml.etree.ElementTree as ET

engine = create_engine('sqlite:///keepass.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

tree = ET.parse('k.xml')
root = tree.getroot()
empty = [ ]

for child in root:
   group = child.find('./title').text
   for children in child.findall("./group"):
       servername = children.find('./title').text
       entries = children.findall('./entry')
       for e in entries:
           data = {}
           data["group"] = group
           data["servername"] = servername
           data["username"] = e.find('username').text
           data["password"] = e.find('password').text
           data["ip"] = e.find("url").text
           data["comment"] = e.find("comment").text
           empty.append(data)
       #import to database directly.

 
for i in empty:
     server = Host(servername=i["servername"], ip=i["ip"], port="0000", group=i["group"])
     session.add(server)
     session.commit()
     passwd = Passwd(username=i["username"], password=i["password"], host=server)
     session.add(passwd)
     session.commit()
