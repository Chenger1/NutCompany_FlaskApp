from flask import Blueprint

public = Blueprint('public', __name__)

from .site_views import *
