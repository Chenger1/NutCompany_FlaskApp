from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, URL, Optional, Email
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


class CorporateClientForm(FlaskForm):
    photo = FileField('Photo')
    text = TextAreaField('Text', validators=[DataRequired()])


class AboutCompanyForm(FlaskForm):
    text = TextAreaField('Text')


class AboutCompanyGalleryForm(FlaskForm):
    photo = FileField('Photo', validators=[validate_photo])


class ContactsForm(FlaskForm):
    office_address = StringField('Адрес офиса ')
    manufacture = StringField('Адрес производства')
    main_phone = StringField('Основной телефон')
    add_phone = StringField('Дополнительный телефон')
    telegram = StringField('Telegram')
    viber = StringField('Viber')
    whats_up = StringField('What`s up')
    email = StringField('E-mail', validators=[Email()])
    map = TextAreaField('Код карты')
