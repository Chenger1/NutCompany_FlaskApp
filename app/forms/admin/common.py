from flask_wtf import FlaskForm
from wtforms.fields import (StringField, TextAreaField, HiddenField, FloatField, BooleanField, DateTimeField,
                            IntegerField, RadioField, SelectField)
from wtforms.validators import DataRequired, URL, Optional, Email, InputRequired
from wtforms import ValidationError

from app._db.choices import DeliveryTypeChoice, PaymentChoice, OrderStatusChoice

from ..custom_field import DateTimeLocalHTML5FormatField, CustomFileField

from datetime import datetime


def validate_photo(form, field):
    if not field.data and not hasattr(form, 'obj'):
        raise ValidationError('Photo - is required')


class NewsItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    photo = CustomFileField('Photo', validators=[InputRequired()])
    publication_date = DateTimeLocalHTML5FormatField('Date', validators=[DataRequired()])


class NewsItemEditForm(NewsItemForm):
    photo = CustomFileField('Photo')


class GalleryForm(FlaskForm):
    photo = CustomFileField('Photo', validators=[validate_photo])
    url = StringField('URL', validators=[URL(), Optional()])
    text = TextAreaField('Текст', validators=[Optional()])

    def validate_text(self, field):
        if field.data and self.url.data:
            raise ValidationError('Нельзя одновременно указывать и текст и ссылку')


class FormsetManagementForm(FlaskForm):
    counter = HiddenField('FORMSET_COUNTER')


class CorporateClientForm(FlaskForm):
    photo = CustomFileField('Photo')
    text = TextAreaField('Text', validators=[DataRequired()])


class AboutCompanyForm(FlaskForm):
    text = TextAreaField('Text')


class AboutCompanyGalleryForm(FlaskForm):
    photo = CustomFileField('Photo', validators=[validate_photo])


class ContactsForm(FlaskForm):
    office_address = StringField('Адрес офиса ')
    manufacture = StringField('Адрес производства')
    main_phone = StringField('Основной телефон')
    add_phone = StringField('Дополнительный телефон')
    telegram = StringField('Telegram')
    viber = StringField('Viber')
    whats_up = StringField('What`s up')
    email = StringField('E-mail', validators=[Email()])
    map = TextAreaField('Код карты')


class ProductForm(FlaskForm):
    weight = StringField('Масса нетто')
    energy = StringField('Энергетическая ценность')
    condition = TextAreaField('Условия хранения')
    desc = TextAreaField('Описание')
    package = CustomFileField('Изображение упаковки')
    desc_image = CustomFileField('Изображение для описания')
    promo_price = FloatField('Акционная цена', validators=[Optional()])
    is_promo = BooleanField('Акционный товар', default=False)
    date = DateTimeField('Добавлен')
    amount = IntegerField('Количество товаров')

    def validate_date(self, field):
        field.data = datetime.now()


class CreateProductForm(ProductForm):
    type = StringField('Тип продукта', validators=[DataRequired()])
    name = StringField('Имя продукта', validators=[DataRequired()])
    composition = StringField('Состав', validators=[DataRequired()])
    life = StringField('Срок годности', validators=[DataRequired()])
    price = FloatField('Цена, грн.', validators=[DataRequired()])


class EditProductForm(ProductForm):
    type = StringField('Тип продукта')
    name = StringField('Имя продукта')
    composition = StringField('Состав')
    life = StringField('Срок годности')
    price = FloatField('Цена, грн.')


class ProductGalleryForm(FlaskForm):
    photo = CustomFileField('Изображение', validators=[validate_photo])


class EditOrderForm(FlaskForm):
    number = IntegerField('Номер заказа', validators=[Optional()])
    fio = StringField('ФИО клиента', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Номер телефона', validators=[DataRequired()])

    address = StringField('Адрес доставки', validators=[DataRequired()])
    city = StringField('Город доставки', validators=[DataRequired()])

    delivery_type = RadioField('Способ доставки', choices=DeliveryTypeChoice.choices(),
                               coerce=DeliveryTypeChoice.coerce)
    payment = RadioField('Способ платежа', choices=PaymentChoice.choices(),
                         coerce=PaymentChoice.coerce)
    status = SelectField('Статус заказа', choices=OrderStatusChoice.choices(),
                         coerce=OrderStatusChoice.coerce)
    sum = FloatField('Сумма заказа', validators=[Optional()])

    date = DateTimeField('Дата создания', validators=[Optional()])
