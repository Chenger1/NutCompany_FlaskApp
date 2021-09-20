from . import main

from app._db import site_models
from app.forms.admin.formset import Formset, InlineFormset
from app.forms.admin import common

from app.utils.generic import FormsetGenericMixin, InlineFormsetMixin, UpdateViewMixin, DetailInstanceMixin
from app.utils.mixins import AdminMethodView


class GalleryPageView(AdminMethodView, FormsetGenericMixin):
    template_name = 'admin/pages/gallery_page.html'
    formset_class = Formset(common.GalleryForm, site_models.MainPageGallery, extra=1)
    redirect_url = 'main.gallery_page'
    model = site_models.MainPageGallery


class CorporateClientsView(AdminMethodView, FormsetGenericMixin):
    template_name = 'admin/pages/corporate_client_page.html'
    formset_class = Formset(common.CorporateClientForm, site_models.CorporateClients, extra=0)
    redirect_url = 'main.corporate_clients_page'
    model = site_models.CorporateClients


class AboutCompanyView(AdminMethodView, InlineFormsetMixin):
    template_name = 'admin/pages/about_company_page.html'
    form_class = common.AboutCompanyForm
    formset_class = InlineFormset(form_class=common.AboutCompanyGalleryForm,
                                  model=site_models.AboutCompanyGallery, extra=1)
    redirect_url = 'main.about_company_page'
    model = site_models.AboutCompanyGallery
    entity_model = site_models.AboutCompany

    def get_entity_instance(self, obj_id=None):
        instance = self.entity_model.query.first()
        if not instance:
            return self.entity_model()
        return instance


class AboutCompanyViewDetail(AdminMethodView, DetailInstanceMixin):
    model = site_models.AboutCompany
    template_name = 'admin/pages/about_company_page_detail.html'


class ContactsView(AdminMethodView, UpdateViewMixin):
    template_name = 'admin/pages/contacts_page.html'
    model = site_models.Contacts
    form_class = common.ContactsForm
    redirect_url = 'main.contacts_page'

    def get_instance(self, obj_id=None):
        instance = self.model.query.first()
        if not instance:
            return self.model()
        return instance


class CommonSiteSettingsView(AdminMethodView, UpdateViewMixin):
    template_name = 'admin/pages/common_site_settings.html'
    model = site_models.CommonSiteSetting
    form_class = common.CommonSiteSettings
    redirect_url = 'main.common_site_settings'

    def get_instance(self, obj_id=None):
        instance = self.model.query.first()
        if not instance:
            return self.model()
        return instance


main.add_url_rule('/admin/gallery', view_func=GalleryPageView.as_view('gallery_page'))
main.add_url_rule('/admin/corporate_clients', view_func=CorporateClientsView.as_view('corporate_clients_page'))
main.add_url_rule('/admin/about_company', view_func=AboutCompanyView.as_view('about_company_page'))
main.add_url_rule('/admin/about_company/detail/<obj_id>', view_func=AboutCompanyViewDetail.as_view('about_company_detail'),
                  defaults={'obj_id': 1})
main.add_url_rule('/admin/contacts', view_func=ContactsView.as_view('contacts_page'))
main.add_url_rule('/admin/common', view_func=CommonSiteSettingsView.as_view('common_site_settings'))
