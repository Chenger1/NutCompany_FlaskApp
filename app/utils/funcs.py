import os

from werkzeug.utils import secure_filename

from flask_mail import Message
from flask import render_template

from ..config import upload_folder
from app import mail


def handle_files(file_data):
    if isinstance(file_data, str):
        return file_data
    if file_data.filename:
        filename = secure_filename(file_data.filename)
        save_path = os.path.join(upload_folder, filename)
        file_data.save(save_path)
        return filename


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender='Oreh', recipients=[to])
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)
