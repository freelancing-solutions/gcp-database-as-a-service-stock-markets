from flask import Flask
from data_service.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from data_service.api.users.routes import users_bp
    from data_service.api.stocks.routes import stocks_bp
    from data_service.api.settings.routes import settings_bp
    from data_service.handlers.routes import default_handlers_bp
    from data_service.api.pubsub.routes import pubsub_bp
    from data_service.api.scrapper.routes import scrapper_bp
    from data_service.tasks_input_pubsub_handlers.routers import task_bp
    from data_service.frontpage.routes import home_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(scrapper_bp)
    app.register_blueprint(pubsub_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(default_handlers_bp)

    return app
