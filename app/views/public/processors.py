from . import public

from app._db.site_models import Contacts


@public.context_processor
def contacts():
    return {'contacts': Contacts.query.first()}
