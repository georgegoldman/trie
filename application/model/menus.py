from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Menus(db.Model):
    __tablename__='menu'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.Text, nullable=True)
    price = db.Column(db.Text, nullable=False)
    user_id  = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('menu', lazy=True))

    def __init__(self, title, description, picture, price, user_id):
        self.title = title
        self.description = description
        self.picture = picture
        self.price = price
        self.user_id = user_id

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