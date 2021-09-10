from flask_login import login_required
from flask_login.utils import current_user

from werkzeug.exceptions import Forbidden


class LoginRequiredMixin:
    """
        This provides an easy way to mark class-based views as requiring login.
    """
    @login_required
    def dispatch_request(self, *args, **kwargs):
        return getattr(super(LoginRequiredMixin, self), 'dispatch_request')(*args, **kwargs)


class AdminPermissionRequiredMixin:
    """
    Provide easy way to mark class-based views as admin permission required
    """
    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_admin:
            raise Forbidden()
        return getattr(super(AdminPermissionRequiredMixin, self), 'dispatch_request')(*args, **kwargs)
