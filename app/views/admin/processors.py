from . import main

from app._db.models import User

import datetime


@main.context_processor
def new_users_count():
    today = datetime.date.today()
    return {'new_users_count': User.query.filter(User.is_admin==False,
                                                 (User.joined-today) <= 14).count()}
