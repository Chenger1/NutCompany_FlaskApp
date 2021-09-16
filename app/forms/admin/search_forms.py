from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField
from wtforms.validators import Optional

from app._db.choices import OrderStatusChoice, RequestStatusChoice


class OrderSearchForm(FlaskForm):
    start = DateField('start', validators=[Optional()])
    end = DateField('end', validators=[Optional()])
    status = SelectField('Статус', choices=OrderStatusChoice.choices_all(), coerce=OrderStatusChoice.coerce,
                         validators=[Optional()])


class RequestSearchForm(FlaskForm):
    start = DateField('start', validators=[Optional()])
    end = DateField('end', validators=[Optional()])
    phone = StringField('phone', validators=[Optional()])
    fio = StringField('fio', validators=[Optional()])
    status = SelectField('status', choices=RequestStatusChoice.choices_all(),
                         coerce=RequestStatusChoice.coerce, validators=[Optional()])
