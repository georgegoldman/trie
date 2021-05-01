import os, secrets, cloudinary.uploader, cloudinary.api, cloudinary
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from application import db, bcrypt, allowed_file, app
from application.model.user import User
from application.model.triet import Triet
from werkzeug.utils import secure_filename
from PIL import Image

usr = Blueprint('user',__name__)

@usr.route('/')
@usr.route('/home')
@login_required
def home():
    return render_template('home.html')

@usr.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@usr.route('/login', methods=['POST'])
def login_post():
    phone  = request.form.get('phone')
    password = request.form.get('password')
    user = User.query.filter_by(phone=phone).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect('/')
    
    else:
        flash('Please create an account you don\'t have and account in our network ')
        return redirect('/login')

@usr.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@usr.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    phone = request.form.get('phone')
    password = request.form.get('password')
    
    user = User.query.filter_by(phone=phone).first()
    
    if user:
        flash('This phone number is having an account in our network 👀')
        return redirect('/register')
    new_user = User(username=username, phone=phone, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Your account has been succefully created 👊! ')    
    return redirect('/login')

@usr.route('/make_treat', methods=['GET'])
def make_treate__get():
    
    return render_template('make_treat.html')

@usr.route('/create_triet', methods=['POST'])
def create_triet():
    title = request.form.get('title')
    image = request.files['image']
    description = request.form.get('description')
    price = request.form.get('price')
    return {
        'data': {
            'title': title,
            'description': description,
            'price': price
        }
    }

@usr.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')