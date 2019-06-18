"""Extensions to flask app."""

from flask import Flask
from flask.config import Config


class App(Flask):
    config: Config
    pass
