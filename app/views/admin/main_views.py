from flask import render_template

from . import main

from app.utils.mixins import AdminMethodView


class StatisticView(AdminMethodView):
    def get(self):
        return render_template('admin/index.html')


main.add_url_rule('/admin', view_func=StatisticView.as_view('statistic'))
