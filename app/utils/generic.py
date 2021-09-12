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
