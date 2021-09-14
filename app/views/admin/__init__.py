from flask import Blueprint

main = Blueprint('main', __name__)
admin_auth = Blueprint('admin_auth', __name__, url_prefix='/admin_auth')

from . import main_views, admin_auth_views, users_views, news_views, page_settings_views, product_views
