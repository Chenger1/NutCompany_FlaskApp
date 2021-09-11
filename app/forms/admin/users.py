from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email


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
    photo = StringField('Photo', validators=[DataRequired()])
