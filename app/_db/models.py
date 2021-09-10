from app import db

from enum import Enum


class UserTypeChoice(Enum):
    legal_person = 'Юридическое лицо'
    physical_person = 'Физические лицо'


class DeliveryTypeChoice(Enum):
    new_mail = 'Новая почта (по Украине, оплата за счет Клиента)'
    courier = 'Куръер по Одесса'
    self_pickup = 'Самовывоз со склада'


class PaymentChoice(Enum):
    privat = 'LiqPay/Приват24'
    cashless = 'Безналичный расчет'
    cash = 'Наличными при получении (Наложенным платежом)'


class OrderStatusChoice(Enum):
    unpaid = 'Неоплачен'
    in_progress = 'В обработке'
    sent = 'Отправлен'
    done = 'Выполнен'


class RequestStatusChoice(Enum):
    in_progress = 'В обработке'
    closed = 'Отказано'
    done = 'Выполнен'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    photo = db.Column(db.String())
    joined = db.Column(db.Date())

    # This fields are only for admin
    is_admin = db.Column(db.Boolean(), default=False)

    # This fields are only for client
    country = db.Column(db.String(30), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    index = db.Column(db.String(20), nullable=True)
    type = db.Column(db.Enum(UserTypeChoice))
    credentials = db.Column(db.String(30), nullable=True)

    orders = db.relationship('Order', backref='user')


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

    gallery = db.relationship('ProductGallery', backref='product')


class ProductGallery(db.Model):
    __tablename__ = 'product_gallery'

    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.Integer(), db.ForeignKey('product.id'))


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

    items = db.relationship('OrderItem', backref='order')


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
