from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email


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
    password = PasswordField('Password')
    password2 = PasswordField('Password2')

    is_admin = BooleanField(default=True)
