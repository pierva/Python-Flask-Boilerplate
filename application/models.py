import datetime
import json

from application import db, flask_bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    password = db.Column(db.String(64), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password).\
            decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)

    @property
    def serialize_user(self):
        return {
            'id': self.id,
            'email': self.email
            }
