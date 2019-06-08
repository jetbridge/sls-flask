"""Main Flask app configuration file.

Creates a new instance of our Flask app with plugins, blueprints, views, and configuration loaded.
"""
import os
import logging
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.core import patcher, xray_recorder
from werkzeug.contrib.fixers import ProxyFix
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import request
from .db import db
from .secret import get_secret
from .api import api, init_views
from .commands import init_cli
from .flask import App

log = logging.getLogger(__name__)


def create_app(test_config=None) -> App:
    app = App("TEMPLATE")

    # load config
    configure(app=app, test_config=test_config)

    # extensions
    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    configure_database(app)
    api.init_app(app)  # flask-rest-api

    # CLI
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)  # migrations under "flask db"
    init_cli(app, manager)

    init_views()
    init_xray(app)
    init_auth(app)

    return app


def init_auth(app):
    jwt = JWTManager(app)

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        from TEMPLATE.model.user import User

        if identity is None:
            return None
        user = User.query.get(identity)
        if user:
            user.current_region = request.headers.get(app.config["REGION_HEADER_NAME"])
        return user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        ret = {"msg": "User {} not found".format(identity)}
        from flask import jsonify

        return jsonify(ret), 404

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        assert user.id
        return user.id


def configure_database(app):
    """Set up flask with SQLAlchemy."""
    db.init_app(app)  # init sqlalchemy
    app.migrate = Migrate(app, db)  # alembic

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Close session after request.

        Ensures no open transactions remain.
        """
        db.session.remove()


def configure_class(app):
    config_class = os.getenv("TEMPLATE_CONFIG".upper())

    if not config_class:
        # figure out which config to load
        if os.getenv("AWS_EXECUTION_ENV"):
            # running in AWS
            stage = os.getenv("STAGE")
            if stage == "prod":
                config_class = "TEMPLATE.config.ProdConfig"
            else:
                config_class = "TEMPLATE.config.DevConfig"
        else:
            # local dev
            config_class = "TEMPLATE.config.LocalDevConfig"

    app.config.from_object(config_class)


def configure_secrets(app):
    if app.config.get("LOAD_SECRETS"):
        # fetch config secrets from Secrets Manager
        secret_name = app.config["SECRET_NAME"]
        secrets = get_secret(secret_name=secret_name)
        if secrets:
            log.debug(f"{len(secrets.keys())} secrets loaded")
            app.config.update(secrets)
        else:
            log.debug("Failed to load secrets")


def configure_instance(app):
    # load 'instance.cfg'
    # if it exists as our local instance configuration override
    app.config.from_pyfile("instance.cfg", silent=True)


def configure(app: App, test_config=None):
    configure_class(app)
    config = app.config
    if test_config:
        config.update(test_config)
    else:
        configure_secrets(app)
        configure_instance(app)

    # use 'DATABASE_URL' config for SQLAlchemy
    if "DATABASE_URL" in config and "SQLALCHEMY_DATABASE_URI" not in config:
        config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URL"]

    if config.get("SQLALCHEMY_ECHO"):
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from .config import check_valid

    if not check_valid(config):
        raise Exception("Configuration is not valid.")


def init_xray(app: App):
    if not app.config.get("XRAY"):
        return
    patcher.patch(("requests", "boto3"))  # xray tracing for external requests
    xray_recorder.configure(service="TEMPLATE")
    XRayMiddleware(app, xray_recorder)
