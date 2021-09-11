from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

from wtforms import StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email

from app._db.models import User


class AdminEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 150),
                                             Email()])
    fio = StringField('FIO', validators=[DataRequired(),
                                         Length(1, 150)])
    phone = StringField('Phone', validators=[DataRequired(),
                                             Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])

    is_admin = BooleanField(default=True)
    photo = FileField('Photo', validators=[FileRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('User with this email already exists')
