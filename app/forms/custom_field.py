from wtforms.fields.html5 import DateTimeLocalField
from wtforms import FileField, ValidationError

from app.utils.funcs import handle_files

import datetime


def validate_photo_file_allowed(form, field):
    if field.data:
        extension = field.data.split('.')[-1]
        if extension not in ('png', 'jpeg', 'jpg'):
            raise ValidationError('Допустимые форматы фото: png, jpg, jpeg')


class DateTimeLocalHTML5FormatField(DateTimeLocalField):
    def process_formdata(self, valuelist):
        if valuelist:
            data_str = ' '.join(valuelist)
            html5_format_date = datetime.datetime.strptime(data_str, '%Y-%m-%dT%H:%M')
            html5_format_date_str = datetime.datetime.strftime(html5_format_date, self.format)
            try:
                self.data = datetime.datetime.strptime(html5_format_date_str, self.format)
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid datetime value'))


class CustomFileField(FileField):
    """
    Save instance to upload directory at set file path as field value
    """
    def process_formdata(self, valuelist):
        if valuelist:
            filename = handle_files(valuelist[0])
            if filename:
                self.data = filename

    def validate(self, form, extra_validators=tuple()):
        return super().validate(form, (*extra_validators, validate_photo_file_allowed))
