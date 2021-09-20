import os

from environs import Env
from pathlib import Path

env = Env()
env.read_env()

base_dir = Path(__file__).parent
upload_folder = os.path.join(base_dir, 'uploads')

render_as_batch = bool(int(env.str('RENDER_BATCH')))


class Config:
    SECRET_KEY = env.str('SECRET_KEY') or 'test string'
    MAIL_SERVER = env.str('MAIL_SERVER')
    MAIL_USERNAME = env.str('MAIL_USERNAME')
    MAIL_PASSWORD = env.str('MAIL_PASSWORD')
    MAIL_FROM = env.str('MAIL_FROM')
    MAIL_PORT = env.str('MAIL_PORT')
    MAIL_USE_TLS = bool(int(env.str('MAIL_USE_TLS')))
    MAIL_SENDER = env.str('MAIL_SENDER')
    UPLOAD_FOLDER = upload_folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = env.str('DEV_DB_URL') or 'sqlite:///' + os.path.join(base_dir, 'dev.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = env.str('DEV_DB_URL') or 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')


config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
