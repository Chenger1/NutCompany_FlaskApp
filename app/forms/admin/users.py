from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import fields, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, InputRequired

from app._db.models import User
from app._db.choices import CountryChoice, UserTypeChoice
from app.forms.custom_field import CustomFileField

from datetime import date


class UserBaseForm(FlaskForm):
    email = fields.StringField('Email', validators=[DataRequired(),
                                                    Length(1, 150),
                                                    Email()])
    fio = fields.StringField('FIO', validators=[DataRequired(),
                                                Length(1, 150)])
    phone = fields.StringField('Phone', validators=[DataRequired(),
                                                    Length(1, 30)])
    photo = CustomFileField('Photo', validators=[InputRequired(),
                                                 FileAllowed({'png', 'jpg', 'jpeg'})])

    def validate_password(self, field):
        if field.data != self.password2.data:
            raise ValidationError('Passwords are different')


class AdminEditForm(UserBaseForm):
    photo = CustomFileField('Photo', validators=[FileAllowed({'png', 'jpg', 'jpeg'})])

    password = fields.PasswordField('Password')
    password2 = fields.PasswordField('Password2')

    is_admin = fields.BooleanField(default=True)


class AdminCreateForm(UserBaseForm):
    password = fields.PasswordField('Password', validators=[DataRequired()])
    password2 = fields.PasswordField('Password2', validators=[DataRequired()])

    is_admin = fields.BooleanField(default=True)
    joined = fields.DateField('Joined')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User with this email already exists')
        return field

    def validate_joined(self, field):
        field.data = date.today()
        return field


class ClientAdminPageForm(FlaskForm):
    fio = fields.StringField('??????', validators=[DataRequired()])
    email = fields.StringField('Email', validators=[Email()])
    phone = fields.StringField('?????????? ????????????????', validators=[DataRequired()])
    country = fields.SelectField('????????????', choices=CountryChoice.choices(), coerce=CountryChoice.coerce)
    city = fields.StringField('??????????')
    address = fields.StringField('??????????')
    index = fields.IntegerField('????????????', validators=[Optional()])
    type = fields.SelectField('??????', choices=UserTypeChoice.choices(), coerce=UserTypeChoice.coerce)
    credentials = fields.TextAreaField('??????????????????')
    photo = CustomFileField('????????', validators=[FileAllowed({'png', 'jpg', 'jpeg'})])

    country_ur = fields.SelectField('???????????? ????????????????', choices=CountryChoice.choices(), coerce=CountryChoice.coerce)
    city_ur = fields.StringField('?????????? ????????????????')
    address_ur = fields.StringField('?????????? ????????????????')
    company = fields.StringField('????????????????')

    personal_discount = fields.IntegerField('???????????????????????? ????????????, %', validators=[Optional()])
