import os, secrets, cloudinary.uploader, cloudinary.api, cloudinary
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from application import db, bcrypt, allowed_file, app
from application.model.eatery import User
from application.model.menus import Menus
from werkzeug.utils import secure_filename
from PIL import Image

usr = Blueprint('user',__name__)

@usr.route('/')
@usr.route('/home')
@login_required
def home():
    return render_template('home.html')

@usr.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@usr.route('/register', methods=['GET'])
def register():
    return render_template('register.html')