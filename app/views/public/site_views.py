from . import public
from flask.views import MethodView
from flask import render_template, jsonify

from app._db.models import Product
from app._db.site_models import NewsItem, AboutCompany, MainPageGallery
from app.utils.generic import DetailInstanceMixin


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


class GalleryView(MethodView):
    model = MainPageGallery

    def get(self, limit=None):
        if limit:
            instances = self.model.query.limit(int(limit))
        else:
            instances = self.model.query.all()
        return jsonify({'items': self.serialize(instances)})

    def serialize(self, query):
        result = []
        for item in query:
            result.append({
                'id': item.id,
                'photo': item.photo,
                'url': item.url
            })
        return result


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
public.add_url_rule('/about', view_func=AboutCompanyView.as_view('about_page'), defaults={'obj_id': 1})

public.add_url_rule('/gallery', view_func=GalleryView.as_view('gallery_view'))
public.add_url_rule('/gallery/<limit>', view_func=GalleryView.as_view('gallery_view_with_limit'))
