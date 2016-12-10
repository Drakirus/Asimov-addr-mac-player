#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import commands
reload(sys)
sys.setdefaultencoding('utf8')

from datetime import datetime


from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    #  id en auto-incrementing
    name = CharField()
    fistname = CharField()
    ip = CharField(null = True)
    mac = CharField(null = True)
    team = CharField(null = True)
    pizza = CharField(null = True)

db.connect()
try:
    db.create_tables([User])
except Exception as e:
    print e

UPLOAD_FOLDER = './uploads'
app = Flask(__name__, static_url_path = "", static_folder = "contents")
app.config.from_object(__name__)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'asimov' and password == 'tagada72'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

class RegistrationForm(Form):
    name = StringField('Nom', [validators.Length(min=3, max=25)])
    fistname = StringField('Prenom', [validators.Length(min=3, max=35)])
    team = StringField('Team name', [validators.Length(min=3, max=35)])
    pizza = StringField('Pizza', [validators.Length(min=3, max=35)])


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('register'))

@app.route('/ok', methods=['GET'])
def ok():
    return render_template('index.html')


@app.route('/db')
@requires_auth
def db():
    return render_template('db.html', User=User.select(), remove=remove)

@app.route('/delete/<int:id>', methods=['POST'])
@requires_auth
def remove(id):
    """Delete an uploaded file."""
    q = User.delete().where(User.id == id)
    try:
        q.execute()
    except Exception as e:
        return e
    return redirect(url_for('db'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        mac = commands.getstatusoutput('./arpfind.sh ' + request.remote_addr)
        User.create(name=form.name.data, fistname=form.fistname.data, ip=request.remote_addr, team=form.team.data, pizza=form.pizza.data).save
        return redirect(url_for('ok'))
    return render_template('register.html', form=form)

@app.route('/uploads/<path:path>')
def proxy(path):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

