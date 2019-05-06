import os

CONFIG_EXPECTED_KEYS = ('DATABASE_URL', 'OPENAPI_VERSION')


class Config:
    """Base config."""
    # load more config from secrets manager?
    LOAD_SECRETS = False  # skip secrets manager for local/test by default

    # this will come from secrets manager when running in AWS
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql:///TEMPLATE')  # use local "TEMPLATE" DB for local dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # set this to echo queries to stderr
    # broken: https://github.com/pallets/flask-sqlalchemy/issues/724
    SQLALCHEMY_ECHO = os.getenv('SQL_ECHO', False)

    DEBUG = os.getenv('DEBUG', False)

    # print SQL queries
    DUMP_SQL = os.getenv('DUMP_SQL', False)

    # openapi can be found at /api/openapi.json /api/doc
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/api'
    OPENAPI_JSON_PATH = 'openapi.json'
    OPENAPI_REDOC_PATH = '/doc'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_SWAGGER_UI_VERSION = '3.22.0'
    # https://swagger.io/docs/specification/authentication/bearer-authentication/
    API_SPEC_OPTIONS = {
        'components': {
            'securitySchemes': {
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                },
            }
        },
        'security': [
            {
                'bearerAuth': []
            },
        ]
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'INSECURE')


class LocalDevConfig(Config):
    """Local development environment config."""
    DEBUG = True


class DevConfig(Config):
    """AWS dev environment and DB."""
    LOAD_SECRETS = True
    # name of Secrets Manager secretID for config
    SECRET_NAME = 'TEMPLATE/dev'


class ProdConfig(Config):
    """AWS dev environment and DB."""
    LOAD_SECRETS = True
    # name of Secrets Manager secretID for config
    SECRET_NAME = 'TEMPLATE/prod'


# config checks


class ConfigurationInvalidError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message + f"\nEnvironment: {os.environ}"


class ConfigurationKeyMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} key in configuration.")


class ConfigurationValueMissingError(ConfigurationInvalidError):
    def __init__(self, key: str):
        super().__init__(message=f"Missing {key} value in configuration.")


def check_valid(conf) -> bool:
    """Check if config looks okay."""

    def need_key(k):
        if k not in conf:
            raise ConfigurationKeyMissingError(k)
        if not conf.get(k):
            raise ConfigurationValueMissingError(k)

    [need_key(k) for k in CONFIG_EXPECTED_KEYS]
    return True


def check_valid_handler(event, context):
    # which env are we checking?
    config_class = event.get('env', 'TEMPLATE.config.LocalDevConfig')

    # create an app with this config
    from .flask import App
    app = App(__name__)
    app.config.from_object(config_class)
    conf = app.config

    ok = check_valid(conf)

    return dict(ok=ok, )
