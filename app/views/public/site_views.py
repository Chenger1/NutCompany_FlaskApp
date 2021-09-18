from . import public
from flask.views import MethodView

from app._db.models import Product
from app._db.site_models import NewsItem, AboutCompany, MainPageGallery, CorporateClients
from app.utils.generic import DetailInstanceMixin, ListMixinApi, ListViewMixin, TemplateMixin

from .filters import truncate_html_filter

import datetime


class IndexPageView(MethodView, TemplateMixin):
    template_name = 'public/index.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context.update({
            'products': Product.query.all(),
            'news': NewsItem.query.limit(6),
            'about': AboutCompany.query.first()
        })
        return context


class AboutCompanyView(MethodView, DetailInstanceMixin):
    template_name = 'public/about.html'
    model = AboutCompany

    def get_instance(self, obj_id):
        return self.model.query.first()

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['news'] = NewsItem.query.limit(6)
        return context


class GalleryPageView(MethodView, TemplateMixin):
    template_name = 'public/gallery.html'


class GalleryView(MethodView, ListMixinApi):
    model = MainPageGallery
    paginate_by = 6

    def get_serialized_item(self, item):
        return {'id': item.id,
                'photo': item.photo,
                'url': item.url}


class NewsApiView(MethodView, ListMixinApi):
    model = NewsItem
    paginate_by = 4

    def get_serialized_item(self, item):
        return {'id': item.id,
                'title': item.title,
                'text': truncate_html_filter(item.text, 250),
                'photo': item.photo,
                'publication_date': item.publication_date.strftime('%d.%m.%Y')}

    def get_instances(self):
        """ Return new that are published """
        return self.model.query.filter(self.model.publication_date <= datetime.datetime.now())


class NewsPageView(MethodView, TemplateMixin):
    template_name = 'public/news_page.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['gallery_image'] = MainPageGallery.query.first()
        return context


class DetailNewsItemView(MethodView, DetailInstanceMixin):
    model = NewsItem
    template_name = 'public/one-new.html'

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['last_news'] = self.model.query.order_by().limit(3).all()
        return context


class CorporateClientsView(MethodView, ListViewMixin):
    model = CorporateClients
    template_name = 'public/customers.html'
    paginate_by = 5


class ContactsPageView(MethodView, TemplateMixin):
    template_name = 'public/contacts_page.html'


class PaymentView(MethodView, TemplateMixin):
    template_name = 'public/payments.html'


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
public.add_url_rule('/about', view_func=AboutCompanyView.as_view('about_page'), defaults={'obj_id': 1})
public.add_url_rule('/gallery_page', view_func=GalleryPageView.as_view('gallery_page'))
public.add_url_rule('/news', view_func=NewsPageView.as_view('news_page'))
public.add_url_rule('/news/<obj_id>', view_func=DetailNewsItemView.as_view('news_detail'))
public.add_url_rule('/customers', view_func=CorporateClientsView.as_view('customers_page'))
public.add_url_rule('/contacts', view_func=ContactsPageView.as_view('contacts_page'))

public.add_url_rule('/gallery', view_func=GalleryView.as_view('gallery_view'))
public.add_url_rule('/news_api', view_func=NewsApiView.as_view('news_api_view'))
