from flask.views import MethodView
from flask import render_template

from . import admin_auth


class AdminLogin(MethodView):
    def get(self):
        return render_template('admin/login.html')


admin_auth.add_url_rule('/login', view_func=AdminLogin.as_view('admin_login'))
