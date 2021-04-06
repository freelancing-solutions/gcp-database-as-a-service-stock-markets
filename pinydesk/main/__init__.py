from flask import Flask
from pinydesk.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from pinydesk.api.users.routes import users_bp
    from pinydesk.api.stocks.routes import stocks_bp
    from pinydesk.api.settings.routes import settings_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(settings_bp)

    return app
