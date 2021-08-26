# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

from flask  import Flask, render_template, request, redirect, flash, url_for
# from flask_login import login_required, current_user

from .models import Hypervisor
# from .config import DATABASE
from pylxd import Client

import json
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE

# main = Blueprint('main', __name__)


client = Client(endpoint=os.getenv("SERVERLXD"),
                cert=(os.getenv("CERTPATH"), os.getenv("KEYPATH")))
client.authenticate(os.getenv("SERVERSEC"))
# client.trusted

# @login_required
@app.route('/')
def index():
    try:
        with open('hypinfo.json', 'r') as f:
            uname = json.loads(f.read())
    except:
        uname = {
            "system": "None",
            "node": "None",
            "release": "None",
            "version": "None",
            "machine": "None",
            "processor": "None"
        }
    hypervisor = Hypervisor(
        uname['system'],
        uname['node'],
        uname['release'],
        uname['version'],
        uname['machine'],
        uname['processor']
        )

    containers = []

    try:
        # client = Client(endpoint=SERVERLXD)
        # client.authenticate(SERVERSEC)
        # client.trusted
        containers = client.instances.all()
    except Exception as e:
        print(e)
    return render_template('index.html', containers=containers, hypervisor=hypervisor) 

@app.route('/container/<name>', methods=['POST', 'GET'])
def container(name):
    # client = Client()
    container = client.containers.get(name)
    if request.method == 'POST':
        container.start()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

@app.route('/upload/iso')
def add_iso():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        # distr = request.form['distr']
        # arch = request.form['arch']
        # version = request.form['version']
        # public = True if request.form.get('public') else False

        if name == '':
            flash('Поля должны быть заполнены')
            return redirect(url_for('upload_iso'))
    return render_template('create_vm.html')

@app.route('/create/vm', methods=['POST', 'GET'])
def create_vm_local():
    if request.method == 'POST':
        name = request.form['name']
        iso = request.form['iso']

        if name == '' or iso == '':
            flash('Поля должны быть заполнены')
            return redirect(url_for('create_vm_local'))

        try:
            config = {
                'name': name, 
                'source': {'type': 'image', 'alias': iso}}
            # client = Client()
            instance = client.instances.create(config, wait=True)
            instance.start()
        except Exception as e:
            flash(str(e))
            return redirect(url_for('create/vm'))

        return redirect(url_for('index'))
    # client = Client()
    images = client.images.all()
    return render_template('create_vm.html', images=images)

@app.route('/download/iso', methods=['POST', 'GET'])
def create_vm_url():
    if request.method == 'POST':
        pass
    
    return render_template('download_iso.html')

