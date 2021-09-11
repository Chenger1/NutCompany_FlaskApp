from flask.views import MethodView
from flask import render_template, redirect, flash, url_for
from flask_login import login_user, logout_user

from . import admin_auth

from app._db.models import User
from app.forms.admin.auth import AdminLoginForm
from app.utils.mixins import LoginRequiredMixin, AdminPermissionRequiredMixin


class AdminLogin(MethodView):
    def get(self):
        form = AdminLoginForm()
        return render_template('admin/login.html', form=form)

    def post(self):
        form = AdminLoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.verify_password(form.password.data) and user.is_admin:
                login_user(user)
                return redirect(url_for('main.statistic'))
        flash('Или у вас неверные данные или нет прав доступа')
        return render_template('admin/login.html', form=form)


class AdminLogout(LoginRequiredMixin, AdminPermissionRequiredMixin, MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('main.statistic'))


admin_auth.add_url_rule('/login', view_func=AdminLogin.as_view('admin_login'))
admin_auth.add_url_rule('/logout', view_func=AdminLogout.as_view('admin_logout'))
