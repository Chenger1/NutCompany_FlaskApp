from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired, Optional


class RequestForm(FlaskForm):
    fio = StringField('ФИО', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    date = DateTimeField('Дата', validators=[Optional()])
    status = StringField('Статус', validators=[Optional()])
