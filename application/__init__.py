from datetime import timedelta
import os, cloudinary
import http.client
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(__name__)

app.config["JWT_SECRET_KEY"] = '8bd58efcb4f77f95fa30b0e72232ec5b'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ALGORITHM"] = "HS512"
app.config["JWT_DECODE_ALGORITHMS"] = "HS512"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=5)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# app.config["JWT_PRIVATE_KEY"] = open('jwt-key').read()
jwt = JWTManager(app)

CORS(app, resources={r'/*': {"origins": "*"}})

# UPLOAD_FOLDER = '/home/yashuayaweh/Documents/PROGRAMMING/lifeat/application/static/imgs/menu'
ALLOWED_EXTENSIONS = {'png',     'jpg', 'jpeg'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.'in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)

bcrypt = Bcrypt(app)

app.config['DEBUG'] = False
if os.environ.get('FLASK_ENV') == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

print(f'ENV is set to: {app.config["ENV"]}')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


db = SQLAlchemy(app)
Migrate = Migrate(app, db)
# login_manager = LoginManager(app)

from .model.user import User
from .model.triet import Triet

app.config["JWT_SECRET_KEY"] = "fdngiu43895u32609#~@@{"


@jwt.user_lookup_loader
def user_identity_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

# db.create_all()JWT Locations

from .route import user
app.register_blueprint(user.usr)

