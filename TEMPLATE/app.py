"""Contains global app instance, not created unless explicitly imported."""
from .create_app import create_app
from .api import init_views

app = create_app()
init_views()

__all__ = ("app",)
