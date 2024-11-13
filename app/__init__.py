from flask import Flask


def create_app():
  app = Flask(__name__)
  app.config.from_object("config")

  with app.app_context():
    from . import views

    from app.posts import post_bp
    app.register_blueprint(post_bp)

    from app.users import user_bp
    app.register_blueprint(user_bp)
  return app