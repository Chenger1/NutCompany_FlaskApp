from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from app.config import config_dict, render_as_batch

from .views.error_handling import error_handler

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(render_as_batch=render_as_batch)
login_manager = LoginManager()
login_manager.login_view = 'admin_auth.admin_login'


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    config_dict[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .views.admin import main as admin_main, admin_auth
    from .views import common
    from ._db import models, site_models

    app.register_blueprint(admin_main)
    app.register_blueprint(admin_auth)
    app.register_blueprint(common)

    app.register_error_handler(HTTPException, error_handler)

    return app
