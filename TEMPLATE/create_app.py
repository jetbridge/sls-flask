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


log = logging.getLogger(__name__)


# logging
# FIXME: set this from env?
# logging.basicConfig(level=logging.DEBUG)


def create_app(test_config=None) -> App:
    app = App(__name__)

    # load config
    configure(app=app, test_config=test_config)

    # extensions
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    db.init_app(app)  # init sqlalchemy
    app.db = db
    app.migrate = Migrate(app, db)  # alembic
    api.init_app(app)  # flask-rest-api

    # scripts
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)  # migrations under "flask db"

    load_views(app)

    return app


def load_views(self):
    """Register blueprints and routes."""
    from .views import register_blueprints

    for blp in register_blueprints:
        api.register_blueprint(blp)


def configure(app: App, test_config=None):
    config_class = os.getenv('TEMPLATE_CONFIG'.upper())

    if not config_class:
        # figure out which config to load
        if os.getenv('AWS_EXECUTION_ENV'):
            # running in AWS
            stage = os.environ['STAGE']
            if stage == 'prod':
                config_class = 'TEMPLATE.config.ProdConfig'
            else:
                config_class = 'TEMPLATE.config.DevConfig'
        else:
            # local def
            config_class = 'TEMPLATE.config.LocalDevConfig'

    app.config.from_object(config_class)

    if app.config.get('LOAD_SECRETS'):
        # fetch config secrets from Secrets Manager
        secret_name = app.config['SECRET_NAME']
        secrets = get_secret(secret_name=secret_name)
        if secrets:
            log.debug(f"{len(secrets.keys())} secrets loaded")
            app.config.update(secrets)
        else:
            log.debug("Failed to load secrets")

    if test_config:
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config.get("DUMP_SQL"):
        print("Enabling query logging")
        print(f"Connected to database {app.config['SQLALCHEMY_DATABASE_URI']}")
        logging.basicConfig()
        # query logging
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    from .config import check_valid
    if not check_valid(app.config):
        raise Exception("Configuration is not valid.")
