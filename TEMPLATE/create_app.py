"""Main Flask app configuration file.

Creates a new instance of our Flask app with plugins, blueprints, views, and configuration loaded.
"""
import os
from .flask import App
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix
import logging
from .database import db
from .secret import get_secret
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from .api import api
from .commands import init_cli

log = logging.getLogger(__name__)

# logging
# FIXME: set this from env?
# logging.basicConfig(level=logging.DEBUG)


def create_app(test_config=None) -> App:
    app = App('TEMPLATE')

    # load config
    configure(app=app, test_config=test_config)

    # extensions
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    configure_database(app)
    api.init_app(app)  # flask-rest-api

    # CLI
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)  # migrations under "flask db"
    init_cli(app, manager)

    load_views(app)

    return app


def configure_database(app):
    """Set up flask with SQLAlchemy."""
    db.init_app(app)  # init sqlalchemy
    app.db = db
    app.migrate = Migrate(app, db)  # alembic

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()


def load_views(self):
    """Register blueprints and routes."""
    from .views import register_blueprints

    for blp in register_blueprints:
        api.register_blueprint(blp)


def configure_class(app):
    config_class = os.getenv('TEMPLATE_CONFIG'.upper())

    if not config_class:
        # figure out which config to load
        if os.getenv('AWS_EXECUTION_ENV'):
            # running in AWS
            stage = os.getenv('STAGE')
            if stage == 'prod':
                config_class = 'TEMPLATE.config.ProdConfig'
            else:
                config_class = 'TEMPLATE.config.DevConfig'
        else:
            # local def
            config_class = 'TEMPLATE.config.LocalDevConfig'

    app.config.from_object(config_class)


def configure_secrets(app):
    if app.config.get('LOAD_SECRETS'):
        # fetch config secrets from Secrets Manager
        secret_name = app.config['SECRET_NAME']
        secrets = get_secret(secret_name=secret_name)
        if secrets:
            log.debug(f"{len(secrets.keys())} secrets loaded")
            app.config.update(secrets)
        else:
            log.debug("Failed to load secrets")


def configure_instance(app):
    # load 'TEMPLATE/instance.cfg'
    # if it exists as our local instance configuration override
    app.config.from_pyfile('instance.cfg', silent=True)


def configure(app: App, test_config=None):
    configure_class(app)
    config = app.config
    if test_config:
        config.update(test_config)
    else:
        configure_secrets(app)
        configure_instance(app)

    # use 'DATABASE_URL' config for SQLAlchemy
    if 'DATABASE_URL' in config and 'SQLALCHEMY_DATABASE_URI' not in config:
        config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']

    if config.get("SQLALCHEMY_ECHO"):
        print("Enabling query logging")
        print(f"Connected to database {app.config['SQLALCHEMY_DATABASE_URI']}")

    from .config import check_valid
    if not check_valid(config):
        raise Exception("Configuration is not valid.")
