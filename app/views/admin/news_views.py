from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteInstanceMixin
from app._db.site_models import NewsItem

from app.forms.admin.common import NewsItemForm, NewsItemEditForm

from . import main

from datetime import datetime


class NewsListView(AdminMethodView, ListViewMixin):
    model = NewsItem
    template_name = 'admin/news/news_list.html'


class CreateNewItemView(AdminMethodView, CreateViewMixin):
    model = NewsItem
    form_class = NewsItemForm
    template_name = 'admin/news/news_detail.html'
    redirect_url = 'main.news_list'


class UpdateNewsItemView(AdminMethodView, UpdateViewMixin):
    model = NewsItem
    form_class = NewsItemEditForm
    template_name = 'admin/news/news_detail.html'
    redirect_url = 'main.news_list'

    def get_context(self, form, instance):
        context = super().get_context(form, instance)
        context['old_date'] = datetime.strftime(instance.publication_date, '%Y-%m-%dT%H:%M')
        return context


class DeleteNewsItem(AdminMethodView, DeleteInstanceMixin):
    model = NewsItem
    redirect_url = 'main.news_list'


main.add_url_rule('/admin/news_list', view_func=NewsListView.as_view('news_list'))
main.add_url_rule('/admin/news/create', view_func=CreateNewItemView.as_view('create_news'))
main.add_url_rule('/admin/news_detail/<obj_id>', view_func=UpdateNewsItemView.as_view('edit_news'))
main.add_url_rule('/admin/news_detail/<obj_id>/delete', view_func=DeleteNewsItem.as_view('delete_news'))
