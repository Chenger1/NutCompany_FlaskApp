from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Optional

from app._db.choices import CountryChoice, UserTypeChoice
from ..custom_field import CustomFileField


class ClientRegistrationForm(FlaskForm):
    fio = StringField('ФИО*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Телефон*', validators=[DataRequired()])
    photo = CustomFileField('Загрузить фото', validators=[DataRequired()])

    country = SelectField('Страна', choices=CountryChoice.choices(), coerce=CountryChoice.coerce,
                          validators=[Optional()])
    city = StringField('Город*', validators=[DataRequired()])
    address = StringField('Адрес', validators=[Optional()])

    password = StringField('Пароль*', validators=[DataRequired()])

    credentials = StringField('Реквизиты', validators=[Optional()])

    country_fop = SelectField('Страна', choices=CountryChoice.choices(), coerce=CountryChoice.coerce,
                              validators=[Optional()])
    city_fop = StringField('Город*', validators=[Optional()])
    address_fop = StringField('Адрес', validators=[Optional()])
    index = StringField('Индекс', validators=[Optional()])

    type = RadioField('Тип', choices=UserTypeChoice.choices(), coerce=UserTypeChoice.coerce,
                      validators=[Optional()])
