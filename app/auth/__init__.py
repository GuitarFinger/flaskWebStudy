from flask import Blueprint  # 蓝本

auth = Blueprint('auth', __name__)

from . import views
