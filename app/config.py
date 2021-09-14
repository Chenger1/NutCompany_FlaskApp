import os

from environs import Env
from pathlib import Path

env = Env()
env.read_env()

base_dir = Path(__file__).parent
upload_folder = os.path.join(base_dir, 'uploads')


class Config:
    SECRET_KEY = env.str('SECRET_KEY') or 'test string'
    UPLOAD_FOLDER = upload_folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = env.str('DEV_DB_URL') or 'sqlite:///' + os.path.join(base_dir, 'dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    RENDER_AS_BATCH = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = env.str('DEV_DB_URL') or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
