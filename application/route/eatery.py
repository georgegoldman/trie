from flask import Blueprint, render_template, request, redirect
from application import db
from application.model.eatery import User
from application.model.menus import Menus
from flask_login import login_required

eat = Blueprint('eat',__name__)

@eat.route('/eat')
def eatery():
    return 'hi'

@eat.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@eat.route('/register', methods=['POST'])
def register_post():
    email  = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    
    check_user = User.query.filter_by(email=email).first()
    if check_user and check_user.username == username:
        return redirect('/login')
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return 'user created'

@eat.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@eat.route('/login', methods=['POST'])
def login_post():
    return render_template('login.html')