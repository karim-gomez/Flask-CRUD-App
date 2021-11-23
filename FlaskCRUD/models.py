from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from FlaskCRUD import db, login


# Set up user_loader
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), index=True, unique=True)
    username = db.Column(db.String(30), index=True)
    password_hash = db.Column(db.String(128))
    product = db.relationship('Product', backref='owned_user', lazy="dynamic")
    # backref allows us to kno which users created the product
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable.')

    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)


class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    price = db.Column(db.Integer())
    description = db.Column(db.String(200))
    pro_created = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
