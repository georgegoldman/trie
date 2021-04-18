from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Menus(db.Model):
    __tablename__='menu'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    price = db.Column(db.Text, nullable=False)
    user_id  = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('menu', lazy=True))

    def __init__(self, name, email, price, user_id):
        self.name = name
        self.email = email
        self.price = price
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'{self.name}'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'price': self.price,
            'user_id': self.user_id
        }