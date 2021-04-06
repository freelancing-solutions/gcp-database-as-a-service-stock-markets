from flask import Flask
from pinoydesk.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from pinoydesk.api.users.routes import users_bp
    from pinoydesk.api.stocks.routes import stocks_bp
    from pinoydesk.api.settings.routes import settings_bp
    from pinoydesk.handlers.routes import default_handlers_bp
    from pinoydesk.tasks_input_pubsub_handlers.routers import task_bp
    
    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(default_handlers_bp)

    return app
