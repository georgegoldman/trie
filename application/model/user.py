from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from sqlalchemy.types import Enum
import  enum
import uuid


class User(db.Model, UserMixin):
    __tableusername__='user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=True)
    profile_px = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)
    accountType = db.Column(db.String(80), default='personal')
    instagram = db.Column(db.Text, nullable=True)
    youtube  = db.Column(db.Text, nullable=True)
    twitter = db.Column(db.Text, nullable=True)
    website = db.Column(db.Text, nullable=True)
    menus = db.relationship('Triet', backref=db.backref('user', lazy=True))

    def __init__(self, username, phone, password):
        self.username = username
        self.phone = phone
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self) -> str:
        return f'{self.username}'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'phone' : self.password,
            'email' : self.email,
            'profile_px': self.profile_px,
            'password': self.password,
        }