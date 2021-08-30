# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

from flask  import Flask, render_template, request, redirect, flash, url_for
# from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from src import tools 
# from .config import DATABASE
from pylxd import Client

import json
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv("UPLOAD_FOLDER")
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE

# main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'tar.gz'}
try:
    client = Client(
        endpoint=os.getenv("REMOTE_HOST"), 
        cert=(os.getenv("CERT_PATH"), os.getenv("KEY_PATH")),
        verify=os.getenv("VERIFY_SSL"),
        )
    client.authenticate(os.getenv("PASSWORD"))
except Exception as e:
    print("ERROR:", e)


# @login_required
@app.route('/')
def index():
    
    containers = {}
    hypervisor = tools.getHypervisor()
    try:
        containers = client.containers.all()
    except Exception as e:
        print("ERROR:", e)
    return render_template('index.html', containers=containers, hypervisor=hypervisor) 

@app.route('/container/<name>', methods=['POST', 'GET'])
def container(name):
    if request.method == 'POST':
        container = client.containers.get(name)
        container.start()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)
    
@app.route('/container/<name>/stop', methods=['POST'])
def container_stop(name):
    if request.method == 'POST':
        container = client.containers.get(name)
        container.stop()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

@app.route('/container/<name>/start', methods=['POST'])
def container_start(name):
    if request.method == 'POST':
        container = client.containers.get(name)
        container.start()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

@app.route('/container/<name>/reboot', methods=['POST'])
def container_restart(name):
    if request.method == 'POST':
        container = client.containers.get(name)
        container.restart()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

@app.route('/container/<name>/freeze', methods=['POST'])
def container_freeze(name):
    if request.method == 'POST':
        container = client.containers.get(name)
        container.freeze()
        return redirect(url_for('index'))
    return render_template('container.html', container=container)

def allowed_file(filename):
    return 'tar' in filename.split(".")

@app.route('/upload/iso', methods=['POST', 'GET'])
def upload_iso():
    if request.method == 'POST':
        name = request.form['title']
        desc = request.form['desc']
        data = request.files['mainfile']
        
        if name == '':
            flash('Поля должны быть заполнены')
            return redirect(url_for('upload_iso'))
        elif data.filename == '':
            flash('Файл не выбран')
            return redirect(url_for('upload_iso'))

        if data and allowed_file(data.filename):
            upload_folder = os.getenv("UPLOAD_FOLDER")
            filename = secure_filename(data.filename)
            file_path = os.path.join(upload_folder, filename)
            print(filename)
            data.save(file_path)
            image_data = open(file_path, 'rb').read()
            client.images.create(image_data, public=True, wait=True)
        else:
            flash(f'Файл не подходит: {ALLOWED_EXTENSIONS}')
            return redirect(url_for('upload_iso'))
        return redirect(url_for('index'))

    return render_template('upload_iso.html')

@app.route('/create/vm', methods=['POST', 'GET'])
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
            instance = client.containers.create(config, wait=False)
            instance.start()
        except Exception as e:
            flash(str(e))
            return redirect(url_for('create_vm'))

        return redirect(url_for('index'))
    
    images = {}
    try:
        images = client.images.all()
    except Exception as e:
        print("ERROR:", e)
    return render_template('create_vm.html', images=images)

@app.route('/download/iso', methods=['POST', 'GET'])
def download_iso():
    if request.method == 'POST':
        pass
    
    return render_template('download_iso.html')

