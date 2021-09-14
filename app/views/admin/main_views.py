from flask import render_template, redirect, url_for, flash
from flask.views import MethodView

from . import main

from app._db.models import Request
from app._db.choices import RequestStatusChoice
from app import db

from app.utils.mixins import AdminMethodView
from app.utils.generic import ListViewMixin


class StatisticView(AdminMethodView):
    def get(self):
        return render_template('admin/index.html')


class RequestView(AdminMethodView, ListViewMixin):
    template_name = 'admin/requests.html'
    model = Request


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
main.add_url_rule('/admin/proceed_request/<obj_id>/<operation>', view_func=ProceedRequestView.as_view('proceed_request'))
