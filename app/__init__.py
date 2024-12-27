from flask import Flask
from .controllers.es_pull_scroll import init_es

def create_app():
    app = Flask(__name__)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    init_es()
    return app
