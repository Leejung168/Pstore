from flask import Flask, render_template, request, redirect, jsonify, url_for, g, flash,abort
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import and_

from flask_login import LoginManager, login_required, login_user,logout_user, UserMixin
from flask import session as s
from models import Base, Host, Passwd, User
import urllib

app = Flask(__name__)

#Create Database Engine
#engine = create_engine('sqlite:///keepass.db')
engine = create_engine('mysql://root:lambert@127.0.0.1:3306/keepass')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Flask-login
app.secret_key = '*XaDt(sfGd{6Qy+4q|.%0j;Fdm5?n!*~'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)


#Check the user name if exist in database
def query_user(username):
    try:
        user=session.query(User).filter_by(name=username).one()
        return user
    except:
        return None

#Check the servername if exist in database, the server must be unique.
def servername_check(server_name):
    try:
        server=session.query(Host).filter_by(servername=server_name).one()
        return server
    except:
        return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    s['next_url'] = request.url
    return redirect('/login')

@login_manager.user_loader
def load_user(userid):
    users = session.query(User).filter_by(id=userid).one()
    return users

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = query_user(username)
        if user is not None and user.verify_password(password):
            login_user(user)
            flash("Logged in successfully.")
            #next = request.args.get('next')
            next = s.get('next_url', '/')
            return redirect(next)
        else:
            return abort(401)
    else:
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('login.html')


# Home Page
@app.route('/')
@login_required
def homepage():
    return render_template('index.html')

# Result Page
@app.route('/result/')
@login_required
def result():
    whole = []
    store={}
    search_keys = request.args.get('search').split()
    if len(search_keys) > 1:
        #First search filed;
        search = search_keys[0]
        #Second search filed which is search user;
        search_user = search_keys[1]
    else:
        search = search_keys[0]
        search_user = None
    try:
        search = "%{0}%".format(search)
        result = session.query(Host).filter(Host.servername.like(search)).all()
        if len(result) >= 1:
            for r in result:
                if search_user is None:
                    passwds = session.query(Passwd).filter_by(passwds_id=r.id).all()
                else:
                    passwds = session.query(Passwd).filter_by(passwds_id=r.id, username=search_user).all()
                for ps in passwds:
                    store = {"host_id":r.id, "servername":r.servername, "ip":r.ip, "port":r.port, "username":ps.username, "password": ps.password, "passwordid":ps.id, "comment": ps.comment}
                    whole.append(store)
                    store = {}
    except:
        pass
    return render_template('result.html', search = whole)


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    password_id = request.form.get('password_id')
    PasswordToDelete = session.query(Passwd).filter_by(id=password_id).one()
    session.delete(PasswordToDelete)
    session.commit()
    return jsonify("Okay")


@app.route('/edit', methods=['GET', 'POST'])
@login_required
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
@login_required
def add():
    if request.method == "POST":
        try:
            if request.form['a_servername']:
                a_servername = request.form.get('a_servername').strip()
                if servername_check(a_servername) is None:
                    return jsonify("Repeated server name.")
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
