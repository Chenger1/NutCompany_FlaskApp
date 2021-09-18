from . import public
from flask.views import MethodView
from flask import render_template

from app._db.models import Product
from app._db.site_models import NewsItem, AboutCompany, MainPageGallery
from app.utils.generic import DetailInstanceMixin, ListMixinApi

from .filters import truncate_html_filter

import datetime


class IndexPageView(MethodView):
    template_name = 'public/index.html'

    def get(self):
        products = Product.query.all()
        news = NewsItem.query.limit(6)
        about = AboutCompany.query.first()
        return render_template(self.template_name, products=products, news=news, about=about)


class AboutCompanyView(MethodView, DetailInstanceMixin):
    template_name = 'public/about.html'
    model = AboutCompany

    def get_instance(self, obj_id):
        return self.model.query.first()

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['news'] = NewsItem.query.limit(6)
        return context


class GalleryPageView(MethodView):
    template_name = 'public/gallery.html'

    def get(self):
        return render_template(self.template_name)


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


class NewsPageView(MethodView):
    template_name = 'public/news_page.html'

    def get(self):
        gallery_image = MainPageGallery.query.first()
        return render_template(self.template_name, gallery_image=gallery_image)


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
public.add_url_rule('/about', view_func=AboutCompanyView.as_view('about_page'), defaults={'obj_id': 1})
public.add_url_rule('/gallery_page', view_func=GalleryPageView.as_view('gallery_page'))
public.add_url_rule('/news', view_func=NewsPageView.as_view('news_page'))

public.add_url_rule('/gallery', view_func=GalleryView.as_view('gallery_view'))
public.add_url_rule('/news_api', view_func=NewsApiView.as_view('news_api_view'))
