from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, render_template, request, redirect, flash, url_for
# from flask_login import login_required, current_user

# from .models import Templates
from .config import DATABASE
from pylxd import Client

import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE

# main = Blueprint('main', __name__)

# @login_required
@app.route('/')
def index():
    client = Client()
    containers = client.containers.all()
    return render_template('index.html', containers=containers)

@app.route('/container/<name>', methods=['POST', 'GET'])
def container(name):
    client = Client()
    container = client.containers.get(name)
    if request.method == 'POST':
        container.start()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

@app.route('/add_iso')
def add_iso():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        distr = request.form['distr']
        arch = request.form['arch']
        version = request.form['version']
        public = True if request.form.get('public') else False

        if name == '' or distr == '' or arch == '' or version == '':
            flash('Поля должны быть заполнены')
            return redirect(url_for('add_iso'))
    return render_template('add_iso.html')

@app.route('/create_vm', methods=['POST', 'GET'])
def create_vm():
    if request.method == 'POST':
        name = request.form['name']
        iso = request.form['iso']

        if name == '' or iso == '':
            flash('Поля должны быть заполнены')
            return redirect(url_for('create_vm'))

        try:
            config = {
                'name': name, 
                'source': {'type': 'image', 'alias': iso}}
            client = Client()
            client.instances.create(config, wait=True)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('create_vm'))

        return redirect(url_for('index'))
    client = Client()
    images = client.images.all()
    return render_template('create_vm.html', images=images)
