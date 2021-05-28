import os, io, math, time, random, secrets, cloudinary.uploader, cloudinary.api, cloudinary

from flask.templating import render_template_string
from flask import Blueprint, render_template, request, redirect, flash, jsonify, make_response
from flask_login import login_required, login_user, logout_user, current_user
from application import db, bcrypt, allowed_file, app
from application.model.user import User
from application.model.triet import Triet
from werkzeug.utils import secure_filename
from PIL import Image

usr = Blueprint('user',__name__)



# heading = "Lorem ipsum dolor sit amet."

# content = """
# Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
# Repellat inventore assumenda laboriosam, 
# obcaecati saepe pariatur atque est? Quam, molestias nisi.
# """

# dbr = list()  # The mock database

# posts = 500  # num posts to generate

# quantity = 20  # num posts to return per request

# for x in range(posts):

#     """
#     Creates messages/posts by shuffling the heading & content 
#     to create random strings & appends to the db
#     """

#     heading_parts = heading.split(" ")
#     random.shuffle(heading_parts)

#     content_parts = content.split(" ")
#     random.shuffle(content_parts)

#     dbr.append([x, " ".join(heading_parts), " ".join(content_parts)])


# @usr.route("/")
# def index():
#     """ Route to render the HTML """
#     return render_template("home.html")


# @usr.route("/load")
# def load():
#     """ Route to return the posts """

#     time.sleep(0.2)  # Used to simulate delay

#     if request.args:
#         counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

#         if counter == 0:
#             print(f"Returning posts 0 to {quantity}")
#             # Slice 0 -> quantity from the db
#             res = make_response(jsonify(dbr[0: quantity]), 200)

#         elif counter == posts:
#             print("No more posts")
#             res = make_response(jsonify({}), 200)

#         else:
#             print(f"Returning posts {counter} to {counter + quantity}")
#             # Slice counter -> quantity from the db
#             res = make_response(jsonify(dbr[counter: counter + quantity]), 200)

#     return res



@usr.route('/')
@usr.route('/home')
@login_required
def home():
    all_triet = Triet.query.all()
    all_triet.reverse()
    return render_template('home.html', all_triet=all_triet)

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
    editImage.thumbnail((400, 400))
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

    return {
        'data': {
            'phone': phone,
            'username': username,
            'accounttype': accounttype,
            'instagram': instagram,
            'youtube': youtube,
            'twitter': twitter,
            'website': website,
        }
    }


@usr.route('/editaccountdetails', methods=['GET'])
@login_required
def edit():
    return render_template('edit.html', current_user=current_user)

@usr.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect('/authlandingpage')