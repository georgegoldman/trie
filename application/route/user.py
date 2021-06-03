import os, io, math, time, random, secrets, cloudinary.uploader, cloudinary.api, cloudinary

from flask.templating import render_template_string
from flask import Blueprint, render_template, request, redirect, flash, jsonify, make_response
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import or_
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

@usr.route('/loadTriets')
@login_required
def load():
    quantity = 10
    all_triet = [i.serialize for i in Triet.query.all()]
    if request.args:
        counter = int(request.args.get("c"))

        if counter == 0:
            res = make_response(
                {'msg': all_triet[0: quantity]}, 200
            )
        elif counter == len(all_triet):
            res = make_response(
                {
                    'msg': []
                }, 200
            )
        else:
            res = make_response(
                {'msg': all_triet[counter: counter + quantity]}, 200
            )
    return res

@usr.route('/page/2')
def page2():
    all_triet = Triet.query.all()
    all_triet.reverse()
    return render_template('home2.html', all_triet=all_triet)

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
@login_required
def make_treate__get():
    
    return render_template('make_treat.html')

@usr.route('/create_triet', methods=['POST'])
@login_required
def create_triet():
    title = request.form.get('title')
    image = request.files['image']
    description = request.form.get('description')
    price = request.form.get('price')
    
    # basewidth = 
    filename = secrets.token_hex(16)+'.jpg'
    in_mem_file = io.BytesIO(image.read())
    editImage = Image.open(in_mem_file)
    # w, h = editImage.size
    # w2, h2 = math.floor(w-((25/100)*w)), math.floor(h-((25/100)*h))
    editImage.thumbnail((100, 100))
    in_mem_file = io.BytesIO()
    editImage.save(in_mem_file, format="jpeg", optimize=True)
    in_mem_file.seek(0)
    
    upload_img = cloudinary.uploader.upload(
        in_mem_file,
        folder = "trie/triets/",
        public_id=filename,
        overwrite = True,
        resource_type = "image"
    )
    img = upload_img['url']
    new_triet = Triet(title = title, description = description, picture = img, price = price)
    db.session.add(new_triet)
    db.session.commit()
    
    flash('Your triet has been added 😋')
    return redirect('/home')
    # return {
    #     'h': h,
    #     'w': w
    # }

@usr.route('/triet/<id>', methods=['GET'])
def triet_id(id):
    getTreat = Triet.query.get(id)
    return render_template('trietview.html', triet=getTreat)

@usr.route('/wallet', methods=['GET'])
def wallet():
    return render_template('wallet.html')

@usr.route('/authlandingpage')
def authlandingpage():
    return render_template('authlandingpage.html')

@usr.route('/user_profile')
@login_required
def user_profile():
    return render_template('user_profil.html', current_user=current_user)
    
@usr.route('/updateuserprofilepix')
@login_required
def updateuserprofilepix():
    users = User.query.filter_by(profile_px=None).all()
    for user in users:
        getuser = user.query.filter_by(username=user.username).first()
        getuser.profile_px = "https://res.cloudinary.com/ukony/image/upload/v1622147875/user_prwunp.svg"
        db.session.add(getuser)
    db.session.commit()
    return 'update successful 👊'

@usr.route('/editaccountdetails', methods=['POST'])
@login_required
def editaccountdetails():
    #personal data 
    upload_profile_px = request.files['profile_px']
    phone = request.form.get('phone')
    username = request.form.get('username')
    #account settings
    accounttype = request.form.get('accounttype')
    #socail network
    instagram = request.form.get('instagram')
    youtube = request.form.get('youtube')
    twitter = request.form.get('twitter')
    website = request.form.get('website')

    filename = secrets.token_hex(16)+'.jpg'
    in_mem_file = io.BytesIO(upload_profile_px.read())
    editImage = Image.open(in_mem_file)

    editImage.crop((10, 30, 20, 30))
    in_mem_file = io.BytesIO()
    editImage.save(in_mem_file, format="jpeg", optimize=True)
    in_mem_file.seek(0)

    upload_img = cloudinary.uploader.upload(
        in_mem_file,
        folder = "trie/profile/",
        public_id=filename,
        overwrite = True,
        resource_type = "image"
    )

    img = upload_img['url']

    getUser = User.query.get(current_user.id)
    getUser.username = username
    getUser.phone = phone
    getUser.profile_px = img
    getUser.accountType = accounttype
    getUser.instagram = instagram
    getUser.youtube = youtube
    getUser.twitter = twitter
    getUser.website = website
    db.session.add(getUser)
    db.session.commit()

    flash('Your account details has been updated 😌')
    return redirect('/editaccountdetails')

    # return {
    #     'data': {
    #         'phone': phone,
    #         'username': username,
    #         'accounttype': accounttype,
    #         'instagram': instagram,
    #         'youtube': youtube,
    #         'twitter': twitter,
    #         'website': website,
    #     }
    # }

@usr.route('/search', methods=['GET', ])
@login_required
def search():
    return render_template('search.html', triets=Triet.query.all())

@usr.route('/loadsearch', methods=['GET', ])
@login_required
def loadsearch():
    search_string = request.args.get("str")
    search_triet = [i.serialize for i in Triet.query.filter(Triet.title.contains(search_string) | Triet.description.contains(search_string) | Triet.price.contains(search_string))]
    search_users = [i.serialize for i in User.query.filter(User.username.contains(search_string) | User.phone.contains(search_string) | User.email.contains(search_string))]
    print(search_triet)
    res = make_response(
        {
            'msg': {
                'users': search_users,
                'triet': search_triet
            }
        }, 200
    )

    return res


@usr.route('/editaccountdetails', methods=['GET'])
@login_required
def edit():
    
    return render_template('edit.html', current_user=current_user)

@usr.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/authlandingpage')