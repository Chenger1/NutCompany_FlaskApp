from flask import request, redirect, url_for

from .base_generics import ViewMixin, FormViewMixin

from app import db


class ListViewMixin(ViewMixin):
    paginate_by = 20

    def __init__(self):
        self.pagination = None

    def get_page(self):
        return request.args.get('page', 1, type=int)

    def get_queryset(self):
        query = self.model.query
        return self.paginate(query)

    def paginate(self, query):
        self.pagination = query.paginate(
            self.get_page(), per_page=self.paginate_by,
            error_out=False
        )
        return self.pagination.items

    def get_context(self):
        return {'instances': self.get_queryset(),
                'pagination': self.pagination}

    def get(self):
        context = self.get_context()
        return self.render_template(context)


class UpdateViewMixin(ViewMixin, FormViewMixin):
    redirect_url = None

    def get(self, obj_id):
        instance = self.get_instance(obj_id)
        form = self.get_form(instance)
        context = self.get_context(form, instance)
        return self.render_template(context)

    def post(self, obj_id):
        instance = self.get_instance(obj_id)
        form = self.get_form()
        if form.validate_on_submit():
            self.handle_form(form, instance)
            self.save_instance()
            return redirect(url_for(self.redirect_url))
        context = self.get_context(form, instance)
        return self.render_template(context)

    def get_instance(self, obj_id):
        return self.model.query.get_or_404(obj_id)

    def get_context(self, form, instance):
        return {'form': form, 'instance': instance}


class CreateViewMixin(ViewMixin, FormViewMixin):
    redirect_url = None

    def get(self):
        form = self.get_form()
        context = self.get_context(form)
        return self.render_template(context)

    def post(self):
        form = self.get_form()
        if form.validate_on_submit():
            self.handle_form(form, self.model())
            self.save_instance()
            return redirect(url_for(self.redirect_url))
        context = self.get_context(form)
        return self.render_template(context)

    def get_context(self, form):
        return {'form': form}


class DeleteInstanceMixin:
    model = None
    redirect_url = None

    def get(self, obj_id):
        instance = self.model.query.get_or_404(obj_id)
        db.session.delete(instance)
        db.session.commit()
        return redirect(url_for(self.redirect_url))


class FormsetGenericMixin(ViewMixin):
    formset_class = None
    redirect_url = None

    def get(self):
        queryset = self.get_queryset()
        self.formset_class.queryset = queryset
        formset_state = self.get_formset_get_state()
        context = self.get_context(**formset_state)
        return self.render_template(context)

    def post(self):
        formset_state = self.get_formset_post_state()
        errors = self.formset_class.save()
        if errors:
            context = self.get_context(**formset_state)
            return self.render_template(context)
        return redirect(url_for(self.redirect_url))

    def get_queryset(self):
        return self.model.query.all()

    def get_context(self, **kwargs):
        context = {**kwargs}
        return context

    def get_formset_get_state(self):
        return {
            'formset': self.formset_class.generate_formset(),
            'management_form': self.formset_class.generate_management_form(),
            'empty_form': self.formset_class.empty_form()
        }

    def get_formset_post_state(self):
        return {
            'formset': self.formset_class.get_formset_with_data(request.files, request.form),
            'management_form': self.formset_class.generate_management_form(),
            'empty_form': self.formset_class.empty_form()
        }


class InlineFormsetMixin(FormsetGenericMixin, FormViewMixin):
    entity_model = None
    form_class = None

    def get(self, *args, **kwargs):
        instance = self.get_entity_instance(*args, **kwargs)
        form = self.get_form(instance)
        self.formset_class.queryset = self.get_queryset()
        self.formset_class.entity = instance
        formset_state = self.get_formset_get_state()
        context = self.get_context(**formset_state, main_form=form)
        return self.render_template(context)

    def post(self, *args, **kwargs):
        instance = self.get_entity_instance()
        form = self.get_form(instance)
        formset_state = self.get_formset_post_state()
        if form.validate_on_submit():
            self.handle_form(form, instance)
            self.save_instance()

            errors = self.formset_class.save()
            if not errors:
                return redirect(url_for(self.redirect_url))
        context = self.get_context(**formset_state, main_form=form)
        return self.render_template(context)

    def get_entity_instance(self, obj_id=None):
        if obj_id:
            return self.entity_model.query.get_or_404(obj_id)
        return self.entity_model()
