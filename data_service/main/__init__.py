from flask import Flask
from flask_caching import Cache
from data_service.config import Config

cache_stock_buys_sells:  Cache = Cache(config={'CACHE_TYPE': 'simple'})
# Cache data for six hours- cached data should be volume data
# TODO - there should be a function to purge the cache when not needed
# but normally when the data-service is not being used it will shutdwon and thereby auto purging cache
default_timeout: int = 60*60*6


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cache_stock_buys_sells.init_app(app=app, config={'CACHE_TYPE': 'simple',
                                                     'CACHE_DEFAULT_TIMEOUT': default_timeout})

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
