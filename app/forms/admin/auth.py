from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 150),
                                             Email()]
                        )
    password = PasswordField('Password', validators=[DataRequired()])
