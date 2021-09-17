from flask.views import MethodView

from app.utils.generic import ListViewMixin
from app._db.site_models import MainPageGallery


class GalleryPageView(MethodView, ListViewMixin):
    model = MainPageGallery
    template_name = ''
