from flask import render_template
from flask.views import MethodView

from . import main

from app.utils.mixins import LoginRequiredMixin


class StatisticView(LoginRequiredMixin, MethodView):
    def get(self):
        return render_template('admin/index.html')


main.add_url_rule('/admin', view_func=StatisticView.as_view('statistic'))
