import os, secrets
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from application import db, bcrypt, allowed_file, app
from application.model.eatery import User
from application.model.menus import Menus
from werkzeug.utils import secure_filename
from PIL import Image

eat = Blueprint('eat',__name__)

@eat.route('/eat')
def eatery():
    return 'hi'

@eat.route('/lifeat')
@login_required
def lifeat():
    all_menu = Menus.query.all()
    all_user = User.query.all()
    return render_template('chatting.html', all_menu=all_menu, all_user=all_user)

@eat.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@eat.route('/register', methods=['POST'])
def register_post():
    email  = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    profile_px = request.files['profile_px']
    
    check_user = User.query.filter_by(email=email).first()
    if check_user and check_user.username == username:
        return redirect('/login')
    
    filename = secrets.token_hex(16)+'.jpg'
    profile_px__path = '/home/yashuayaweh/Documents/PROGRAMMING/lifeat/application/static/imgs/profile_px'
    new_user = User(username=username, email=email, profile_px=filename, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    profile_px.save(os.path.join(profile_px__path, filename))
    picture = Image.open(os.path.join(profile_px__path, filename))
    picture.save(os.path.join(profile_px__path  , filename), quality=20, optimize=True)
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
    
    return redirect('/register')

@eat.route('/makemenu', methods=['GET'])
@login_required
def makemenu_get():
    return render_template('makemenu.html')

@eat.route('/makemenu', methods=['POST'])
@login_required
def makemenu_post():
    image = request.files['image']
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    if allowed_file(image.filename):
        filename = secrets.token_hex(16)+'.jpg'
        newMenu = Menus(title=title, description=description, picture=filename, price=price, user_id=current_user.id)
        db.session.add(newMenu)
        db.session.commit()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        picture = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), quality=20, optimize=True)
        # os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], new_name+'.jpg'))
        return redirect(url_for('eat.makemenu_post', filename=filename))
    return request.form

@eat.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    
    return redirect('/')