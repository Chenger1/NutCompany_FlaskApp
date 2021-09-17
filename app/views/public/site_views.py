from . import public
from flask.views import MethodView

from app.utils.generic import ListViewMixin
from app._db.models import Product


class IndexPageView(MethodView, ListViewMixin):
    model = Product
    template_name = 'public/index.html'


public.add_url_rule('/', view_func=IndexPageView.as_view('main_page'))
