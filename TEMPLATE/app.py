"""Contains global app instance, not created unless explicitly imported."""
from .create_app import create_app

app = create_app()

__all__ = ("app",)
