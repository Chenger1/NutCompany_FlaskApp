from app import db
from werkzeug.datastructures import CombinedMultiDict
from wtforms.fields import BooleanField

from app.utils.funcs import handle_files

import copy


class BaseFormset:
    delete_widget = BooleanField

    def __init__(self, form_class, model, queryset=None, extra=1):
        self.model = model
        self.form_class = copy.deepcopy(form_class)  # Original class is safe
        self.queryset = queryset
        self.extra = extra
        self.formset = []

        self.patch_form_with_delete_widget(self.form_class)

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

    def patch_form_with_delete_widget(self, form):
        delete_widget = self.delete_widget('Delete', default=False)
        setattr(form, 'delete', delete_widget)


class Formset(BaseFormset):
    def save(self):
        return self._set_form_data()

    def generate_formset(self):
        self.formset = []
        index = 0
        for index, instance in enumerate(self.queryset):
            form = self.form_class(obj=instance, prefix=f'form-{index}')
            form.obj = instance
            self.formset.append(form)
        else:
            for index, _ in enumerate(range(self.extra), start=index+1 if index > 0 else 0):
                self.formset.append(self.form_class(prefix=f'form-{index}'))
        return self.formset

    def get_formset_with_data(self, formdata, formfiles):
        combined = CombinedMultiDict((formfiles, formdata))
        new_formset = []
        for index, form in enumerate(self.formset):
            if hasattr(form, 'obj'):
                new_form = self.form_class(combined, prefix=f'form-{index}', obj=form.obj)
                new_form.obj = form.obj
            else:
                new_form = self.form_class(combined, prefix=f'form-{index}')
            new_formset.append(new_form)
        self.formset = new_formset
        return self.formset
