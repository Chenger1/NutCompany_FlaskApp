from . import public
from flask.views import MethodView
from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin

from app._db.models import Product, Request
from app._db.site_models import NewsItem, AboutCompany, MainPageGallery, CorporateClients, CommonSiteSetting
from app._db.choices import RequestStatusChoice
from app.utils.generic import DetailInstanceMixin, ListMixinApi, ListViewMixin, TemplateMixin, CreateViewMixin
from app.forms.public.common_forms import RequestForm

from .filters import truncate_html_filter

import datetime


class IndexPageView(MethodView, TemplateMixin):
    template_name = 'public/index.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context.update({
            'products': Product.query.all(),
            'news': NewsItem.query.limit(6),
            'about': AboutCompany.query.first(),
            'site_settings': CommonSiteSetting.query.first()
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
        context['site_settings'] = CommonSiteSetting.query.first()
        return context


class GalleryPageView(MethodView, TemplateMixin):
    template_name = 'public/gallery.html'


class GalleryView(MethodView, ListMixinApi):
    model = MainPageGallery
    paginate_by = 6

    def get_serialized_item(self, item):
        return {'id': item.id,
                'photo': item.photo,
                'url': item.url,
                'text': item.text}


class NewsApiView(MethodView, ListMixinApi):
    model = NewsItem
    paginate_by = 4

    def get_serialized_item(self, item):
        return {'id': item.id,
                'title': item.title,
                'text': truncate_html_filter(item.text, 250),
                'photo': item.photo,
                'publication_date': item.publication_date.strftime('%d.%m.%Y'),
                'url': item.url}

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
    template_name = 'public/payment.html'


class RequestPageView(MethodView, CreateViewMixin):
    model = Request
    template_name = 'public/user/request.html'
    form_class = RequestForm
    redirect_url = 'public.main_page'

    def get_form(self, instance=None):
        form = super().get_form(instance)
        form.date.data = datetime.datetime.now()
        form.status.data = RequestStatusChoice.in_progress
        if request.method == 'GET' and not isinstance(current_user, AnonymousUserMixin):
            form.fio.data = current_user.fio
            form.phone.data = current_user.phone
        return form


class ShopPageView(MethodView, TemplateMixin):
    template_name = 'public/shop/shop.html'

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['about'] = AboutCompany.query.first()
        return context


class ListProductsView(MethodView, ListMixinApi):
    model = Product
    paginate_by = 6

    def get_instances(self):
        return self.model.search(request.args, self.model.query)

    def get_serialized_item(self, item):
        return {'id': item.id,
                'type': item.type,
                'name': item.name,
                'weight': item.weight,
                'price': item.price,
                'is_promo': item.is_promo,
                'is_new': item.is_new,
                'promo_price': item.promo_price,
                'gallery': [gal_item.photo for gal_item in item.gallery[:4]]}


class ProductDetailView(MethodView, DetailInstanceMixin):
    model = Product
    template_name = 'public/shop/product.html'


class ProductCartDetailApi(MethodView):
    model = Product

    def get(self, obj_id):
        instance = self.model.query.get_or_404(obj_id)
        return jsonify(self.serialize(instance))

    def serialize(self, instance):
        return {'id': instance.id,
                'name': instance.name,
                'price': instance.current_sum}


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
public.add_url_rule('/about', view_func=AboutCompanyView.as_view('about_page'), defaults={'obj_id': 1})
public.add_url_rule('/gallery_page', view_func=GalleryPageView.as_view('gallery_page'))
public.add_url_rule('/news', view_func=NewsPageView.as_view('news_page'))
public.add_url_rule('/news/<obj_id>', view_func=DetailNewsItemView.as_view('news_detail'))
public.add_url_rule('/customers', view_func=CorporateClientsView.as_view('customers_page'))
public.add_url_rule('/contacts', view_func=ContactsPageView.as_view('contacts_page'))
public.add_url_rule('/payments', view_func=PaymentView.as_view('payments_page'))
public.add_url_rule('/request', view_func=RequestPageView.as_view('request_page'))

public.add_url_rule('/shop', view_func=ShopPageView.as_view('shop_page'))
public.add_url_rule('/shop/product/<obj_id>', view_func=ProductDetailView.as_view('product_page'))

public.add_url_rule('/gallery', view_func=GalleryView.as_view('gallery_view'))
public.add_url_rule('/news_api', view_func=NewsApiView.as_view('news_api_view'))
public.add_url_rule('/shop_api', view_func=ListProductsView.as_view('products_api_view'))
public.add_url_rule('/product/<obj_id>', view_func=ProductCartDetailApi.as_view('product_cart_api'))
