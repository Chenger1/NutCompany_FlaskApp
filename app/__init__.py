from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from app.config import config_dict

from .views.error_handling import error_handler

db = SQLAlchemy()
migrate = Migrate()
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
    from ._db import models, site_models

    app.register_blueprint(admin_main)
    app.register_blueprint(admin_auth)

    app.register_error_handler(HTTPException, error_handler)

    return app
