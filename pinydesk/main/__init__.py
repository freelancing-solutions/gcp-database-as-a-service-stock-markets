from flask import Flask
import config


def create_app(config_class=config):
    app = Flask(__name__)
    return app