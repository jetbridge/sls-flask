"""CLI commands."""
from .database import db


def init_cli(app, manager):
    if app.debug:
        # seed
        from .database.fixtures import seed_db

        @app.cli.command('seed', help="Seed DB with test data")
        def seed_db_cmd():
            seed_db()
        manager.add_command(seed_db_cmd)

        # init-db (just for local development)
        @app.cli.command('init-db', help="Create DB from model files without running migrations")
        def init_db_cmd():
            db.drop_all(app=app)
            db.create_all(app=app)
            print("Initialized DB")
        manager.add_command(seed_db_cmd)
