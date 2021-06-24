from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash
from .config import DATABASE
from .model import Users
# from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    engine = create_engine(DATABASE)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    email = request.form.get('email')
    password = request.form.get('password')
    user = session.query(Users).filter(Users.email==email).first()


    # Flash это сообщение об ошибке, которое кидается пользователю
    if user:
        flash('Такой Email уже существует')
        return redirect(url_for('auth.signup'))

    new_user = Users(email=email, password=generate_password_hash(password, method='sha256'))
    session.add(new_user)
    session.commit()
    session.close()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    engine = create_engine(DATABASE)
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(Users).filter(Users.email==email).first()

    session.close()
    # Проверка на то что юзер существует и пароль совпадает
    if not user or not check_password_hash(user.password, password):
        flash('Некорректные данные')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))