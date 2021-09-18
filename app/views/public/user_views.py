from . import public

from flask.views import MethodView

from app._db.models import User
from app.forms.public.auth_forms import ClientRegistrationForm
from app.utils.generic import CreateViewMixin


class ClientRegistrationView(MethodView, CreateViewMixin):
    model = User
    template_name = 'public/user/reg-fiz.html'
    redirect_url = 'public.main_page'
    form_class = ClientRegistrationForm


public.add_url_rule('/registration', view_func=ClientRegistrationView.as_view('registration'))
