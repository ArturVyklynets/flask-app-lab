from flask import Flask
from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name="default"):
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  db.init_app(app)
  migrate.init_app(app, db)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  login_manager.login_view = 'users.login'
  login_manager.login_message = 'Please log in to access this page.'
  login_manager.login_message_category = 'warning'



  with app.app_context():
    from . import views
    from app.users.models import User

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    from app.users import user_bp
    app.register_blueprint(user_bp)

  return app