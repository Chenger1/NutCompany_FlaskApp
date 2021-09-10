from flask import render_template
from flask.views import MethodView

from . import main

from app.utils.mixins import LoginRequiredMixin, AdminPermissionRequiredMixin


class AdminUserList(LoginRequiredMixin, AdminPermissionRequiredMixin, MethodView):
    def get(self):
        return render_template('admin/users/admin_users.html')


main.add_url_rule('/admin_list', view_func=AdminUserList.as_view('admin_list'))
