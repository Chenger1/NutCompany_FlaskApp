from flask import send_from_directory

from . import common
from ..config import upload_folder


@common.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(upload_folder, name)
