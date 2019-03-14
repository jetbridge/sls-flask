"""
All views and APIs.

Load all views and export all blueprints for the app in this file.
"""
from .api.monitor import blp as monitor_blueprint


register_blueprints = (
    monitor_blueprint,
)
