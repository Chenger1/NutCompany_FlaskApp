from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import Email, Optional

from ..custom_field import CustomFileField

from app._db.choices import CountryChoice


class ClientPersonalInfoForm(FlaskForm):
    fio = StringField('ФИО', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Телефон', validators=[Optional()])
    company = StringField('Компания', validators=[Optional()])

    photo = CustomFileField('Фото', validators=[Optional()])


class ClientProfileAddressForm(FlaskForm):
    country = SelectField('Страна', choices=CountryChoice.choices(), coerce=CountryChoice.coerce)
    city = StringField('Город', validators=[Optional()])
    address = StringField('Адрес', validators=[Optional()])

    country_ur = SelectField('Страна', choices=CountryChoice.choices(), coerce=CountryChoice.coerce)
    city_ur = StringField('Город', validators=[Optional()])
    address_ur = StringField('Адрес', validators=[Optional()])
    index = StringField('Индекс', validators=[Optional()])
    credentials = StringField('Реквизиты', validators=[Optional()])
