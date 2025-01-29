from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from .config import Config  # Import your Config class

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load the configuration from Config class
    app.config.from_object(Config)  # This loads all the configurations from Config
    app.config['WTF_CSRF_ENABLED'] = False
    db.init_app(app)
    migrate.init_app(app, db)
      # Initialize CSRF protection
    csrf = CSRFProtect(app)
    from .routes import main
    app.register_blueprint(main)

    return app
