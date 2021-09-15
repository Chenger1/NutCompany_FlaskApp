from flask_wtf import FlaskForm
from wtforms import DateField, SelectField
from wtforms.validators import Optional

from app._db.choices import OrderStatusChoice


class OrderSearchForm(FlaskForm):
    start = DateField('start', validators=[Optional()])
    end = DateField('end', validators=[Optional()])
    status = SelectField('Статус', choices=OrderStatusChoice.choices(), coerce=OrderStatusChoice.coerce,
                         validators=[Optional()])
