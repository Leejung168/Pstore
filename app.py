from flask import Flask, render_template, request, redirect, jsonify, url_for, g
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from models import Base, Host, Passwd, User

app = Flask(__name__)

engine = create_engine('sqlite:///keepass.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Home Page
@app.route('/')
def homepage():
    return render_template('index.html')

# Result Page
@app.route('/result/')
def result():
    whole = []
    store={}
    search = request.args.get('search')
    try:
        search = "%{0}%".format(search)
        result = session.query(Host).filter(Host.servername.like(search)).all()
        if len(result) >= 1:
            for r in result:
                passwds = session.query(Passwd).filter_by(passwds_id=r.id).all()
                for ps in passwds:
                    store = {"host_id":r.id, "servername":r.servername, "ip":r.ip, "port":r.port, "username":ps.username, "password": ps.password, "passwordid":ps.id, "comment": ps.comment}
                    whole.append(store)
                    store = {}
    except:
        pass
    return render_template('result.html', search = whole)


@app.route('/delete', methods=['POST'])
def delete():
    password_id = request.form.get('password_id')
    print password_id
    PasswordToDelete = session.query(Passwd).filter_by(id=password_id).one()
    session.delete(PasswordToDelete)
    session.commit()
    return jsonify("Okay")


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == "POST":
        u_hostid = request.form.get('u_hostid')
        # Get the server's ID, because it's primary Key on the hosts.
        hosts_id = u_hostid.split(":")[0]
        # Get the passwd's ID, because it's primary Key on the passwd.
        passwds_id = u_hostid.split(":")[1]
        u_servername = request.form.get('u_servername').strip()
        u_ip = request.form.get('u_ip').strip()
        u_port = request.form.get('u_port').strip()
        u_username = request.form.get('u_username').strip()
        u_password = request.form.get('u_password').strip()
        u_comment = request.form.get('u_comment').strip()
        print "+++" + u_password + "+++"
        try:
            CheckHost = session.query(Host).filter_by(id=hosts_id).one()
            if request.form['u_servername']:
                CheckHost.servername = u_servername
            if request.form['u_ip']:
                CheckHost.ip = u_ip
            if request.form['u_port']:
                CheckHost.port = u_port
            session.add(CheckHost)
            session.commit()
            CheckPass = session.query(Passwd).filter_by(id=passwds_id).one()
            if request.form['u_username']:
                CheckPass.username = u_username
            if request.form['u_password']:
                CheckPass.password = u_password
            if request.form['u_comment']:
                CheckPass.comment = u_comment
            session.add(CheckPass)
            session.commit()
        except:
            return jsonify("Wrong ServerName")
        return jsonify("Okay")
    else:
        return jsonify("Failed")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        try:
            if request.form['a_servername']:
                a_servername = request.form.get('a_servername').strip()
            if request.form['a_ip']:
                a_ip = request.form.get('a_ip').strip()
            if request.form['a_port']:
                a_port = request.form.get('a_port').strip()
            if request.form['a_username']:
                a_username = request.form.get('a_username').strip()
            if request.form['a_password']:
                a_password = request.form.get('a_password').strip()
            if request.form['a_servername']:
                a_servername = request.form.get('a_servername').strip()
            if request.form['a_comment']:
                a_comment = request.form.get('a_comment').strip()
            if request.form['a_servergroup']:
                a_servergroup = request.form.get('a_servergroup').strip()

            server = Host(servername=a_servername, ip=a_ip, port=a_port, group=a_servergroup)
            session.add(server)
            session.commit()
            passwd = Passwd(username=a_username, password=a_password, host=server, comment=a_comment)
            session.add(passwd)
            session.commit()
            print "Done"

        except Exception, e:
            print e
            return jsonify("Failed")
        return jsonify("Okay")
    else:
        return jsonify("No Way!")




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
