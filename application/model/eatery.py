from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
import uuid

class User(db.Model, UserMixin):
    __tableusername__='user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    menus = db.relationship('Menus', backref=db.backref('user', lazy=True))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self) -> str:
        return f'{self.username}'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'password': self.password,
        }