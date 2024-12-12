from flask import Blueprint

user_bp = Blueprint(
  "users",
  __name__,
  url_prefix="/hi",
  template_folder="templates/users",
  static_folder='static'
  )

from . import views