from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

login = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    login.login_view='admin.login'
    login.login_message = 'Log your punk ** in to the website first'
    login.login_message_category='warning'
    
    from .site_blueprint.site import bp as site_bp
    app.register_blueprint(site_bp)

    from .site_blueprint.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    return app