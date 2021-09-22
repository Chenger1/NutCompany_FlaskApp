from flask import render_template, request
from werkzeug.datastructures import CombinedMultiDict

from app import db


class ViewMixin:
    model = None
    template_name = None

    def render_template(self, context):
        return render_template(self.template_name, **context)


class FormViewMixin:
    form_class = None

    def __init__(self):
        self.form = None
        self.instance = None
        self.db = None

    def get_form(self, instance=None):
        if request.method == 'GET':
            form = self.form_class(obj=instance)
        else:
            form = self.form_class(CombinedMultiDict((request.files, request.form)), obj=instance)
        return form

    def handle_form(self, form, instance):
        self.form = form
        self.instance = instance

        for field_name in self.form.data.keys():
            self.handle_field(field_name)

    def handle_field(self, field_name):
        field = getattr(self.form, field_name)

        if field.data or field.data is False:  # Check False for 'checkboxes'
            setattr(self.instance, field_name, field.data)

    def save_instance(self):
        db.session.add(self.instance)
        db.session.commit()
