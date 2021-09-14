from . import main

from app._db.site_models import MainPageGallery, CorporateClients, AboutCompany, AboutCompanyGallery
from app.forms.admin.formset import Formset, InlineFormset
from app.forms.admin.common import GalleryForm, CorporateClientForm, AboutCompanyGalleryForm, AboutCompanyForm

from app.utils.generic import FormsetGenericMixin, InlineFormsetMixin
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


class AboutCompanyView(AdminMethodView, InlineFormsetMixin):
    template_name = 'admin/pages/about_company_page.html'
    form_class = AboutCompanyForm
    formset_class = InlineFormset(form_class=AboutCompanyGalleryForm,
                                  model=AboutCompanyGallery, extra=1)
    redirect_url = 'main.about_company_page'
    model = AboutCompanyGallery
    entity_model = AboutCompany

    def get_entity_instance(self, obj_id=None):
        instance = self.entity_model.query.first()
        if not instance:
            return self.entity_model()
        return instance


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))
main.add_url_rule('/admin/corporate_clients', view_func=CorporateClientsView.as_view('corporate_clients_page'))
main.add_url_rule('/admin/about_company', view_func=AboutCompanyView.as_view('about_company_page'))
