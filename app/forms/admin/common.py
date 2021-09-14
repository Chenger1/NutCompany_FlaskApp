from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, URL, Optional
from wtforms import ValidationError


from ..custom_field import DateTimeLocalHTML5FormatField


def validate_photo(form, field):
    if not field.data and not hasattr(form, 'obj'):
        raise ValidationError('Photo - is required')


class NewsItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    photo = FileField('Photo', validators=[FileRequired()])
    publication_date = DateTimeLocalHTML5FormatField('Date', validators=[DataRequired()])


class NewsItemEditForm(NewsItemForm):
    photo = FileField('Photo')


class GalleryForm(FlaskForm):
    photo = FileField('Photo', validators=[validate_photo])
    url = StringField('URL', validators=[URL(), Optional()])


class FormsetManagementForm(FlaskForm):
    counter = HiddenField('FORMSET_COUNTER')
