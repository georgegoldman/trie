from application import db, bcrypt
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(db.Model):
    __tablename__='user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    triets = db.relationship('Triet', backref=db.backref('user', lazy=True))

    def __init__(self, name, email, password, profile_px):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.profile_px = str.encode(profile_px)

    def __repr__(self) -> str:
        return f'{self.name}'

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password': self.password,
            'profile_px' : self.profile_px.decode('utf-8')
        }