from flask import Blueprint, render_template, request, redirect
from application import db, bcrypt
from application.model.eatery import User
from application.model.menus import Menus
from flask_login import login_required, login_user, logout_user, current_user

eat = Blueprint('eat',__name__)

@eat.route('/eat')
def eatery():
    return 'hi'

@eat.route('/lifeat')
@login_required
def lifeat():
    return render_template('chatting.html')

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

@eat.route('/', methods=['GET'])
def login_get():
    return render_template('login.html', current_user=current_user)

@eat.route('/loginpost', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    search_user = User.query.filter_by(email=email).first()
    if search_user and bcrypt.check_password_hash(search_user.password, password):
        login_user(search_user)
        return redirect('/lifeat')
    
    return 'wrong login details'

@eat.route('/makemenu', methods=['GET'])
@login_required
def makemenu_get():
    return render_template('makemenu.html')

@eat.route('/makemenu', methods=['POST'])
@login_required
def makemenu_post():
    return request.form

@eat.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    
    return redirect('/')