from . import public

from flask.views import MethodView

from app._db.models import User
from app.forms.public.auth_forms import ClientRegistrationForm
from app.utils.generic import CreateViewMixin, TemplateMixin


class ClientRegistrationView(MethodView, CreateViewMixin):
    model = User
    template_name = 'public/user/reg-fiz.html'
    redirect_url = 'public.main_page'
    form_class = ClientRegistrationForm


class TermOfUserView(MethodView, TemplateMixin):
    template_name = 'public/terms-of-use.html'


public.add_url_rule('/registration', view_func=ClientRegistrationView.as_view('registration'))
public.add_url_rule('/terms-of-use', view_func=TermOfUserView.as_view('term_of_use'))
