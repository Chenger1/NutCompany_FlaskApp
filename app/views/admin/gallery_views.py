from . import main

from app._db.site_models import MainPageGallery
from app.forms.admin.formset import Formset
from app.forms.admin.common import GalleryForm

from app.utils.generic import FormsetGenericMixin
from app.utils.mixins import AdminMethodView


class GalleryPageView(AdminMethodView, FormsetGenericMixin):
    template_name = 'admin/pages/gallery_page.html'
    formset_class = Formset(GalleryForm, MainPageGallery, extra=1)
    redirect_url = 'main.gallery_page'
    model = MainPageGallery


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))
