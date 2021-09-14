from . import main

from app._db.site_models import MainPageGallery, CorporateClients
from app.forms.admin.formset import Formset
from app.forms.admin.common import GalleryForm, CorporateClientForm

from app.utils.generic import FormsetGenericMixin
from app.utils.mixins import AdminMethodView


class GalleryPageView(AdminMethodView, FormsetGenericMixin):
    template_name = 'admin/pages/gallery_page.html'
    formset_class = Formset(GalleryForm, MainPageGallery, extra=1)
    redirect_url = 'main.gallery_page'
    model = MainPageGallery


class CorporateClientsView(AdminMethodView, FormsetGenericMixin):
    template_name = 'admin/pages/corporate_client_page.html'
    formset_class = Formset(CorporateClientForm, CorporateClients, extra=0)
    redirect_url = 'main.corporate_clients_page'
    model = CorporateClients


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))
main.add_url_rule('/admin/corporate_clients', view_func=CorporateClientsView.as_view('corporate_clients_page'))
