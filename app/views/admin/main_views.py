from flask import render_template, redirect, url_for, flash
from flask.views import MethodView
from sqlalchemy import not_, extract

from . import main

from app._db.models import Request, User, Order, Product
from app._db.choices import RequestStatusChoice
from app import db
from app.forms.admin.search_forms import RequestSearchForm

from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin

from datetime import datetime


class StatisticView(AdminMethodView):
    def get(self):
        context = {
            'clients': User.query.filter_by(is_admin=False).count(),
            'orders': Order.query.filter(not_(Order.status.like('done'))).count(),
            'products': Product.query.count(),
            'done_orders': self.list_for_statistic_by_month(True),
            'in_progress_orders': self.list_for_statistic_by_month(False)
        }
        return render_template('admin/index.html', **context)

    def list_for_statistic_by_month(self, is_done):
        if is_done is True:
            orders = Order.query.filter(Order.status == 'done')
        else:
            orders = Order.query.filter(not_(Order.status == 'done'))
        result = {}
        for index in range(1, 13):
            result[index] = orders.filter(extract('month', Order.date) == index,
                                          extract('year', Order.date) == datetime.today().year).count()
        return result


class RequestView(AdminMethodView, ListViewMixin):
    template_name = 'admin/requests.html'
    model = Request
    search_form = RequestSearchForm


class ProceedRequestView(AdminMethodView, MethodView):
    model = Request
    redirect_url = 'main.requests'

    def get(self, obj_id, operation):
        instance = self.model.query.get_or_404(obj_id)
        if not hasattr(RequestStatusChoice, operation):
            flash('No such operation')
        else:
            operation_enum = getattr(RequestStatusChoice, operation)
            instance.status = operation_enum
            db.session.add(instance)
            db.session.commit()
        return redirect(url_for(self.redirect_url))


main.add_url_rule('/admin', view_func=StatisticView.as_view('statistic'))
main.add_url_rule('/admin/requests', view_func=RequestView.as_view('requests'))
main.add_url_rule('/admin/proceed_request/<obj_id>/<operation>',
                  view_func=ProceedRequestView.as_view('proceed_request'))
