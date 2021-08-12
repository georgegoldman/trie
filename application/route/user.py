
import os, io, math, random, secrets, cloudinary.uploader, cloudinary.api, cloudinary, datetime
from flask.templating import render_template_string
from flask import Blueprint, render_template, request, redirect, flash, jsonify, make_response
from flask_login import login_required, login_user, logout_user, current_user
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_cors import cross_origin
from sqlalchemy import or_
from application import db, bcrypt, allowed_file, app
from application.model.user import User
from application.model.triet import Triet
from werkzeug.utils import secure_filename
from PIL import Image

usr = Blueprint('user',__name__)


@usr.route('/get_triets', methods=['GET'])
@cross_origin()
@jwt_required()
def get_triets():
    all_triet = [i.serialize for i in Triet.query.all()]
    return {
        'data': all_triet
    }


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    check_user = User.query.filter_by(email=email).first()
    class UserNotExist(Exception):
            def __init__(self, message="This user does not exist"):
                self.message = message
                super().__init__(self.message)
    print(check_user.password)
    if check_user:
        user_password = check_user.password
        pwd_hash = bcrypt.check_password_hash(user_password, password)
        
        if pwd_hash:
            access_token = create_access_token(identity=check_user.id, fresh=datetime.timedelta(minutes=15))
            refresh_token = create_refresh_token(identity=check_user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
    # additional_claims = {"jwt_key": open('jwt-key.pub').read()}
    else:
        raise UserNotExist()

@usr.route('/refresh', methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return {
        "access_token": access_token
    }

@usr.route('/register', methods=['POST'])
def register_post():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email).first()

    if user:
        return {
            'msg': 'Account already exists in our network 👀'
        }
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
        
    return {
        'msg': 'Your account has been succefully created 👊! '
    }

@usr.route('/create_triet', methods=['POST'])
@jwt_required()
def create_triet():
    image = request.files['image']
    description = request.form.get('description')
    title = request.form.get('title')
    amount = request.form.get('amount')
    print(image)

    # change the filename and resize
    filename = secrets.token_hex(16)+'.jpg'
    in_mem_file = io.BytesIO(image.read())
    editImage = Image.open(in_mem_file)
    w, h = editImage.size
    w2, h2 = math.floor(w-((25/100)*w)), math.floor(h-((25/100)*h))
    editImage.thumbnail((w2, h2))
    in_mem_file = io.BytesIO()
    editImage.save(in_mem_file, format="jpeg",quality=90)
    in_mem_file.seek(0)
    #upload the edited image to a cloud storage
    upload_img = cloudinary.uploader.upload(
        in_mem_file,
        folder = os.environ.get('CLOUDINARY_API_FOLDER'),
        public_id=filename,
        overwrite = True,
        resource_type = "image"
    )
    img = upload_img['url']
    new_triet = Triet(title = title, description = description, picture = img, price = amount)
    db.session.add(new_triet)
    db.session.commit()
    return {
        'msg': 'Your triet has been added 😋'
    }

    
@usr.route('/updateuserprofilepix')
def updateuserprofilepix():
    users = User.query.filter_by(profile_px=None).all()
    for user in users:
        getuser = user.query.filter_by(username=user.username).first()
        getuser.profile_px = "https://res.cloudinary.com/ukony/image/upload/v1622147875/user_prwunp.svg"
        db.session.add(getuser)
    db.session.commit()
    return 'update successful 👊'

@usr.route('/editaccountdetails', methods=['POST'])
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
    triets = [i.serialize for i in Triet.query.all()]
    users = [i.serialize for i in User.query.all()]
    # }

@usr.route('/search', methods=['GET', ])
def search():
    return render_template('search.html', triets=Triet.query.all())

@usr.route('/loadsearch', methods=['GET',])
@jwt_required()
def loadsearch():
    search_result = triets + users
    res = make_response(
        {
            'data': search_result
        }, 200
    )

    return res

@usr.route('/getvue_post', methods=['POST'])
def getvue_post():
    if request.method == 'POST':

        return {
            'data': 'request sent'
        }

@usr.route('/loginwith_jwt', methods=['POST'])
def loginwith_jwt():
    email = request.json.get("email")
    password = request.json.get("password")

    print(request.json)

    if email == None and password == None:
        return {
            "msg": "Bad username and password"
        }
    access_token = create_access_token(identity=email)
    return {
        "access_token": access_token
    }
