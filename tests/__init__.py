from flask import current_app
from data_service.config import Config
from data_service.main import create_app

if not current_app:
    app = create_app(config_class=Config)
    app.app_context().push()
else:
    app = current_app

app.testing = True

