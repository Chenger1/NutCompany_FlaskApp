from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config_dict

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    config_dict[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .views.admin import main as admin_main
    from ._db import models, site_models

    app.register_blueprint(admin_main)

    return app
