import getpass

from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)

from . import index, errors, diseases, gmaps, admin_auth, hospitals, users, reports

app.add_url_rule('/', endpoint='index')
app.register_blueprint(diseases.bp)
app.register_blueprint(gmaps.bp)
app.register_blueprint(admin_auth.bp)
app.register_blueprint(hospitals.bp)
app.register_blueprint(users.bp)
app.register_blueprint(reports.bp)


@app.cli.command(with_appcontext=True)
def createadmin():
    username = input('Enter username (default \'admin\'): ')
    if not username.strip():
        username = 'admin'

    while True:
        password = getpass.getpass('Enter password: ')
        password2 = getpass.getpass('Enter password (again): ')
        if password.strip() != password2.strip():
            print('Passwords don\'t match.')
            continue
        if not password.strip():
            print('Password required.')
            continue
        break

    if mongo.db.admin.find_one({'username': username}) is not None:
        print('{} is already a registered admin.'.format(username))
        return

    mongo.db.admin.insert_one({
        'username': username,
        'password': generate_password_hash(password)
    })

    print('User {} registered as admin successfully.'.format(username))
