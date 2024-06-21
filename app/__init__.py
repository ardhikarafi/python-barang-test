from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Konfigurasi database PostgreSQL
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

    return app
