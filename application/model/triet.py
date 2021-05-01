from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
from flask_login import current_user
import uuid

class Triet(db.Model):
    __tablename__='triet'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True)
    price = db.Column(db.Text, nullable=True)
    user_id  = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('triet', lazy=True))

    def __init__(self, title, description, picture, price):
        self.title = title
        self.description = description
        self.picture = picture
        self.price = price
        self.user_id = current_user.id

    def __repr__(self) -> str:
        return f'{self.name}'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'pictute': self.picture,
            'price': self.price,
            
        }