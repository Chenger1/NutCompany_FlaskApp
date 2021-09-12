from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, ValidationError, DateField
from wtforms.validators import DataRequired, Length, Email

from app._db.models import User

from datetime import date


class UserBaseForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 150),
                                             Email()])
    fio = StringField('FIO', validators=[DataRequired(),
                                         Length(1, 150)])
    phone = StringField('Phone', validators=[DataRequired(),
                                             Length(1, 30)])
    photo = FileField('Photo', validators=[FileRequired(),
                                           FileAllowed({'png', 'jpg', 'jpeg'})])

    def validate_password(self, field):
        if field.data != self.password2.data:
            raise ValidationError('Passwords are different')


class AdminEditForm(UserBaseForm):
    photo = FileField('Photo', validators=[FileAllowed({'png', 'jpg', 'jpeg'})])

    password = PasswordField('Password')
    password2 = PasswordField('Password2')

    is_admin = BooleanField(default=True)


class AdminCreateForm(UserBaseForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])

    is_admin = BooleanField(default=True)
    joined = DateField('Joined')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User with this email already exists')
        return field

    def validate_joined(self, field):
        field.data = date.today()
        return field
