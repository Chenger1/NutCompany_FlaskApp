from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, ValidationError
from wtforms.validators import DataRequired, Email, Optional

from app._db.choices import CountryChoice, UserTypeChoice
from app._db.models import User
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

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Пользователем с таким адресом почты уже существует')


class ClientLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Пароль', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = StringField('Текущий пароль', validators=[DataRequired()])
    password = StringField('Новый пароль', validators=[DataRequired()])
    new_password = StringField('Повторите пароль', validators=[DataRequired()])

    def validate_old_password(self, field):
        if not self.instance.verify_password(field.data):
            raise ValidationError('Текущий пароль введен неправильно')

    def validate_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Пароли не совпадают')


class RestorePasswordMailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class RestorePasswordForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired()])
