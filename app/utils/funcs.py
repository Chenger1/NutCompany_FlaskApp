import os

from werkzeug.utils import secure_filename

from ..config import upload_folder


def handle_files(file_data):
    if isinstance(file_data, str):
        return file_data
    if file_data.filename:
        filename = secure_filename(file_data.filename)
        save_path = os.path.join(upload_folder, filename)
        file_data.save(save_path)
        return filename
