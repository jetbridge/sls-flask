"""Extensions to flask app."""

from flask import Flask
from flask.config import Config
from TEMPLATE.config import ConfigurationValueMissingError


class App(Flask):
    config: Config

    def get_config_value_or_raise(self, key):
        """Get a config value or raise an exception if it is not truthy."""
        val = self.config.get(key)
        if val:
            return val
        raise ConfigurationValueMissingError(key)
