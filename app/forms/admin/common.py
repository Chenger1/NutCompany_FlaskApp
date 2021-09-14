from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import (StringField, TextAreaField, HiddenField, FloatField, BooleanField, DateTimeField,
                            IntegerField)
from wtforms.validators import DataRequired, URL, Optional, Email
from wtforms import ValidationError


from ..custom_field import DateTimeLocalHTML5FormatField

from datetime import datetime


def validate_photo(form, field):
    if not field.data and not hasattr(form, 'obj'):
        raise ValidationError('Photo - is required')


class NewsItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired()])
    publication_date = DateTimeLocalHTML5FormatField('Date', validators=[DataRequired()])


class NewsItemEditForm(NewsItemForm):
    photo = FileField('Photo')


class GalleryForm(FlaskForm):
    photo = FileField('Photo', validators=[validate_photo])
    url = StringField('URL', validators=[URL(), Optional()])


class FormsetManagementForm(FlaskForm):
    counter = HiddenField('FORMSET_COUNTER')


class CorporateClientForm(FlaskForm):
    photo = FileField('Photo')
    text = TextAreaField('Text', validators=[DataRequired()])


class AboutCompanyForm(FlaskForm):
    text = TextAreaField('Text')


class AboutCompanyGalleryForm(FlaskForm):
    photo = FileField('Photo', validators=[validate_photo])


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
    package = FileField('Изображение упаковки')
    desc_image = FileField('Изображение для описания')
    promo_price = FloatField('Акционная цена', validators=[Optional()])
    is_promo = BooleanField('Акционный товар', default=False)
    date = DateTimeField('Добавлен')
    amount = IntegerField('Количество')

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
    photo = FileField('Изображение', validators=[validate_photo])
