from flask import render_template

from . import main

from app._db.models import Request

from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin


class StatisticView(AdminMethodView):
    def get(self):
        return render_template('admin/index.html')


class RequestView(AdminMethodView, ListViewMixin):
    template_name = 'admin/requests.html'
    model = Request


main.add_url_rule('/admin', view_func=StatisticView.as_view('statistic'))
main.add_url_rule('/admin/requests', view_func=RequestView.as_view('requests'))
