from flask_login import login_required


class LoginRequiredMixin:
    """
        This provides an easy way to mark class-based views as requiring login.
    """
    @login_required
    def dispatch_request(self, *args, **kwargs):
        return getattr(super(LoginRequiredMixin, self), 'dispatch_request')(*args, **kwargs)
