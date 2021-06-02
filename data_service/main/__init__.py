import functools

from flask import Flask
from flask_caching import Cache
from data_service.config import Config

# TODO find a way to insure errors are not cached

cache_stocks: Cache = Cache(config={'CACHE_TYPE': 'simple'})
cache_affiliates: Cache = Cache(config={'CACHE_TYPE': 'simple'})
cache_memberships: Cache = Cache(config={'CACHE_TYPE': 'simple'})
cache_users: Cache = Cache(config={'CACHE_TYPE': 'simple'})
# Cache data for six hours- cached data should be volume data
# TODO - there should be a function to purge the cache when not needed
# but normally when the data-service is not being used it will shutdown and thereby auto purging cache
default_timeout: int = 60 * 60 * 6


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cache_stocks.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': default_timeout})
    cache_affiliates.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': default_timeout})
    cache_memberships.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': default_timeout})
    cache_users.init_app(app=app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': default_timeout})

    from data_service.api.users.routes import users_bp
    from data_service.api.stocks.routes import stocks_bp
    from data_service.api.settings.routes import settings_bp
    from data_service.api.memberships.routes import memberships_bp
    from data_service.api.affiliates.routes import affiliates_bp
    from data_service.api.coupons.routes import coupons_bp
    from data_service.api.pubsub.routes import pubsub_bp
    from data_service.api.scrapper.routes import scrapper_bp
    from data_service.api.wallet.routes import wallet_bp
    from data_service.handlers.routes import default_handlers_bp
    from data_service.tasks.routers import task_bp
    from data_service.frontpage.routes import home_bp

    app.register_blueprint(wallet_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(memberships_bp)
    app.register_blueprint(affiliates_bp)
    app.register_blueprint(coupons_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(scrapper_bp)
    app.register_blueprint(pubsub_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(default_handlers_bp)

    return app
