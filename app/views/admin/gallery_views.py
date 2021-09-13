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
        management_form = self.formset_class.generate_management_form()
        empty_form = self.formset_class.empty_form()
        return render_template(self.template_name, formset=formset, management_form=management_form,
                               empty_form=empty_form)

    def post(self):
        formset = self.formset_class.get_formset_with_data(request.files, request.form)
        errors = self.formset_class.save()
        management_form = self.formset_class.generate_management_form()
        empty_form = self.formset_class.empty_form()
        if errors:
            return render_template(self.template_name, formset=formset, errors=errors,
                                   management_form=management_form, empty_form=empty_form)
        return redirect(url_for('main.gallery_page'))


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))