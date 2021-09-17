from . import public
from flask.views import MethodView
from flask import render_template

from app._db.models import Product
from app._db.site_models import NewsItem, AboutCompany


class IndexPageView(MethodView):
    template_name = 'public/index.html'

    def get(self):
        products = Product.query.all()
        news = NewsItem.query.limit(6)
        about = AboutCompany.query.first()
        return render_template(self.template_name, products=products, news=news, about=about)


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
