from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField
from wtforms.validators import Email, Optional

from ..custom_field import CustomFileField


class ClientPersonalInfoForm(FlaskForm):
    fio = StringField('ФИО', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Телефон', validators=[Optional()])
    company = StringField('Компания', validators=[Optional()])

    photo = CustomFileField('Фото', validators=[Optional()])
