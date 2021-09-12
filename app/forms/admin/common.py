from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired


from ..custom_field import DateTimeLocalHTML5FormatField


class NewsItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired()])
    publication_date = DateTimeLocalHTML5FormatField('Date', validators=[DataRequired()])


class NewsItemEditForm(NewsItemForm):
    photo = FileField('Photo')
