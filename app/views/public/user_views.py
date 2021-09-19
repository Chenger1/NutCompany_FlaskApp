from . import public

from flask.views import MethodView
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from app._db.models import User
from app.forms.public.auth_forms import ClientRegistrationForm, ClientLoginForm
from app.utils.generic import CreateViewMixin, TemplateMixin


class ClientLoginView(MethodView):
    template_name = 'public/user/enter.html'
    model = User
    form = ClientLoginForm

    def get(self):
        form = self.form()
        return render_template(self.template_name, form=form)

    def post(self):
        form = self.form()
        if form.validate_on_submit():
            user = self.model.query.filter_by(email=form.email.data).first()
            if user and user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('public.main_page'))
        flash('Логин и/или пароль не совпадают')
        return render_template(self.template_name, form=form)


class ClientLogoutView(MethodView):
    redirect_url = 'public.main_page'

    def get(self):
        logout_user()
        return redirect(url_for(self.redirect_url))


class ClientRegistrationView(MethodView, CreateViewMixin):
    model = User
    template_name = 'public/user/reg-fiz.html'
    redirect_url = 'public.main_page'
    form_class = ClientRegistrationForm


class TermOfUserView(MethodView, TemplateMixin):
    template_name = 'public/terms-of-use.html'


public.add_url_rule('/registration', view_func=ClientRegistrationView.as_view('registration'))
public.add_url_rule('/terms-of-use', view_func=TermOfUserView.as_view('term_of_use'))
public.add_url_rule('/login', view_func=ClientLoginView.as_view('login_page'))
public.add_url_rule('/logout', view_func=ClientLogoutView.as_view('logout_page'))
