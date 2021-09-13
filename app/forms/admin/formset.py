from app import db
from werkzeug.datastructures import CombinedMultiDict
from wtforms.fields import BooleanField

from app.utils.funcs import handle_files
from app.forms.admin.common import FormsetManagementForm

import copy


class BaseFormset:
    delete_widget = BooleanField
    management_form_class = FormsetManagementForm

    def __init__(self, form_class, model, queryset=None, extra=1):
        self.model = model
        self.form_class = copy.deepcopy(form_class)  # Original class is safe
        self.queryset = queryset
        self.extra = extra
        self.formset = []
        self.management_form = None
        self._FORMSET_COUNTER = 0

        self.patch_form_with_widgets(self.form_class)

    def _set_form_data(self):
        errors = []
        instances = []
        for form in copy.copy(self.formset):
            if self._is_empty(form.data):
                continue
            if self._is_deleted(form.data):
                self._delete(form)
                continue
            if form.validate():
                instances.append(self._save_form(form))
            else:
                errors.append(form.errors)
        if errors:
            return errors
        db.session.bulk_save_objects(instances)
        db.session.commit()

    def _is_empty(self, form_data):
        form_data.pop('csrf_token')  # csrf_token presents in each form
        return not any(value for value in form_data.values())

    def _is_deleted(self, form_data):
        return form_data.get('delete', False)

    def _delete(self, form):
        db.session.delete(form.obj)
        self.formset.remove(form)

    def _save_form(self, form):
        if hasattr(form, 'obj'):
            instance = form.obj
        else:
            instance = self.model()
        for key, value in form.data.items():
            if key == 'photo':
                value = handle_files(value)
            setattr(instance, key, value)
        return instance

    def patch_form_with_widgets(self, form):
        delete_widget = self.delete_widget('Delete', default=False)
        setattr(form, 'delete', delete_widget)

    def generate_management_form(self):
        self.management_form = self.management_form_class()
        self.management_form.counter.data = self._FORMSET_COUNTER
        return self.management_form


class Formset(BaseFormset):
    def save(self):
        return self._set_form_data()

    def generate_formset(self):
        self.formset = []
        self._FORMSET_COUNTER = 0
        for index, instance in enumerate(self.queryset):
            prefix = f'form-{index}'
            form = self.form_class(obj=instance, prefix=prefix)
            form.obj = instance
            self.formset.append(form)
        else:
            for index, _ in enumerate(range(self.extra), start=self._FORMSET_COUNTER):
                self.formset.append(self.form_class(prefix=f'form-{index}'))
        self._FORMSET_COUNTER = len(self.formset)
        return self.formset

    def get_formset_with_data(self, form_files, form_data):
        combined = CombinedMultiDict((form_files, form_data))
        new_formset = []
        for index, form in enumerate(self.formset):
            prefix = f'form-{index}'
            if hasattr(form, 'obj'):
                new_form = self.form_class(combined, prefix=prefix, obj=form.obj)
                new_form.obj = form.obj
            else:
                new_form = self.form_class(combined, prefix=prefix)
            new_formset.append(new_form)

        # Check for dynamic added formsets
        formset_counter = int(combined.get('counter'))
        # if counter from client bigger than local - new formsets added
        if formset_counter > self._FORMSET_COUNTER:
            for index in range(self._FORMSET_COUNTER, formset_counter+1):
                prefix = f'form-{index}'
                form = self.form_class(combined, prefix=prefix)
                new_formset.append(form)
        self.formset = new_formset
        return self.formset
