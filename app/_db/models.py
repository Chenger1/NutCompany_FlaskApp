from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from .choices import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password_hash = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    photo = db.Column(db.String())
    joined = db.Column(db.Date())

    # This fields are only for admin
    is_admin = db.Column(db.Boolean(), default=False)

    # This fields are only for client
    country = db.Column(db.Enum(CountryChoice), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    index = db.Column(db.String(20), nullable=True)
    type = db.Column(db.Enum(UserTypeChoice))
    credentials = db.Column(db.String(30), nullable=True)

    orders = db.relationship('Order')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('Password it not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    name = db.Column(db.String(100))
    composition = db.Column(db.Text())
    weight = db.Column(db.Integer())
    energy = db.Column(db.Integer())
    life = db.Column(db.Integer())
    condition = db.Column(db.Text())
    desc = db.Column(db.Text())
    package = db.Column(db.String())
    desc_image = db.Column(db.String())
    price = db.Column(db.Float())
    promo_price = db.Column(db.Integer())
    is_promo = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime())

    amount = db.Column(db.Integer())

    gallery = db.relationship('ProductGallery')


class ProductGallery(db.Model):
    __tablename__ = 'product_gallery'

    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.Integer(), db.ForeignKey('product.id'))
    photo = db.Column(db.String())


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'))
    number = db.Column(db.Integer())
    fio = db.Column(db.String(150))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(30))

    date = db.Column(db.DateTime())
    delivery_type = db.Column(db.Enum(DeliveryTypeChoice))
    address = db.Column(db.String(100), nullable=True)

    payment = db.Column(db.Enum(PaymentChoice))
    status = db.Column(db.Enum(OrderStatusChoice))

    sum = db.Column(db.Float())

    items = db.relationship('OrderItem')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer(), db.ForeignKey('product.id'))
    order = db.Column(db.Integer(), db.ForeignKey('order.id'))


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    phone = db.Column(db.String(50))
    fio = db.Column(db.String(100))
    status = db.Column(db.Enum(RequestStatusChoice))
