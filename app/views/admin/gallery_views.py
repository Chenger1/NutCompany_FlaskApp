from . import main

from flask.views import MethodView
from flask import render_template, request, redirect, url_for

from app._db.site_models import MainPageGallery
from app.forms.admin.formset import Formset
from app.forms.admin.common import GalleryForm


class GalleryPageView(MethodView):
    template_name = 'admin/pages/gallery_page.html'
    formset_class = Formset(GalleryForm, MainPageGallery, extra=1)

    def get(self):
        queryset = MainPageGallery.query.all()
        self.formset_class.queryset = queryset
        formset = self.formset_class.generate_formset()
        return render_template(self.template_name, formset=formset)

    def post(self):
        formset = self.formset_class.get_formset_with_data(request.files, request.form)
        errors = self.formset_class.save()
        if errors:
            return render_template(self.template_name, formset=formset, errors=errors)
        return redirect(url_for('main.gallery_page'))


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))
