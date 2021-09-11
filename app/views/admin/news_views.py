from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin
from app._db.site_models import NewsItem

from . import main


class NewsListView(AdminMethodView, ListViewMixin):
    model = NewsItem
    template_name = 'admin/news/news_list.html'


main.add_url_rule('/admin/news_list', view_func=NewsListView.as_view('news_list'))
