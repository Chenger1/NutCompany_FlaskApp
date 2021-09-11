from flask import render_template
from flask.views import MethodView

from . import main

from app.utils.mixins import LoginRequiredMixin, AdminPermissionRequiredMixin
from app._db.models import User


class AdminUserList(LoginRequiredMixin, AdminPermissionRequiredMixin, MethodView):
    def get(self):
        users = User.query.filter_by(is_admin=True).all()
        return render_template('admin/users/admin_users.html', instances=users)


main.add_url_rule('/admin_list', view_func=AdminUserList.as_view('admin_list'))
