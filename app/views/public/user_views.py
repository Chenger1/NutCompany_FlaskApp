from . import public

from flask.views import MethodView
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from app._db.models import User, OrderItem
from app.forms.public.auth_forms import ClientRegistrationForm, ClientLoginForm
from app.forms.public.profile_forms import ClientPersonalInfoForm, ClientProfileAddressForm
from app.utils.generic import CreateViewMixin, TemplateMixin, UpdateViewMixin, DetailInstanceMixin


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


class ShowClientOrdersHistory(MethodView, DetailInstanceMixin):
    model = User
    template_name = 'public/user/orders_history.html'

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['order_item'] = OrderItem
        return context


class ClientProfileMixin(MethodView, UpdateViewMixin):
    def make_request(self):
        return url_for(self.redirect_url, obj_id=self.instance.id)


class ShowClientContactsInfoForPhysicalPerson(ClientProfileMixin):
    """
    Render info if client is not a part of some company
    """
    model = User
    template_name = 'public/user/info-fiz.html'
    form_class = ClientPersonalInfoForm
    redirect_url = 'public.personal_info'


class ShowClientContactsInfoForLegalPerson(ClientProfileMixin):
    """
    Render info if client is a part of some company
    """
    model = User
    template_name = 'public/user/info-ur.html'
    form_class = ClientPersonalInfoForm
    redirect_url = 'public.personal_info_ur'


class ShowClientAddressForPhysicalPerson(ClientProfileMixin):
    model = User
    template_name = 'public/user/address.html'
    form_class = ClientProfileAddressForm
    redirect_url = 'public.personal_address_fop'


class ShowClientAddressForLegalPerson(ClientProfileMixin):
    model = User
    template_name = 'public/user/address-details.html'
    form_class = ClientProfileAddressForm
    redirect_url = 'public.personal_address_ur'


public.add_url_rule('/registration', view_func=ClientRegistrationView.as_view('registration'))
public.add_url_rule('/terms-of-use', view_func=TermOfUserView.as_view('term_of_use'))
public.add_url_rule('/login', view_func=ClientLoginView.as_view('login_page'))
public.add_url_rule('/logout', view_func=ClientLogoutView.as_view('logout_page'))

public.add_url_rule('/profile/<obj_id>/orders', view_func=ShowClientOrdersHistory.as_view('profile'))
public.add_url_rule('/profile/<obj_id>/info/fop',
                    view_func=ShowClientContactsInfoForPhysicalPerson.as_view('personal_info'))
public.add_url_rule('/profile/<obj_id>/info/ur',
                    view_func=ShowClientContactsInfoForLegalPerson.as_view('personal_info_ur'))
public.add_url_rule('/profile/<obj_id>/address/fop',
                    view_func=ShowClientAddressForPhysicalPerson.as_view('personal_address_rop'))
public.add_url_rule('/profile/<obj_id>/address/ur',
                    view_func=ShowClientAddressForLegalPerson.as_view('personal_address_ur'))
