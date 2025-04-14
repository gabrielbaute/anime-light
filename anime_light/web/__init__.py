import os
from flask import Flask
from anime_light.web.routes import index_bp
from anime_light.web.server_config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(index_bp, url_prefix='/')

    @app.context_processor
    def inject_app_name():
        return dict(
            app_name=app.config['APP_NAME'],
            app_version=app.config['APP_VERSION'],
            app_repository=app.config['APP_REPOSITORY'],
            )

    return app