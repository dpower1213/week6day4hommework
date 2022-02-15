from flask import Blueprint
bp = Blueprint('site',__name__,url_prefix='/')
from .import routes