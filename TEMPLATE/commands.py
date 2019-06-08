"""CLI commands."""
from .db import db


def init_cli(app, manager):
    if app.debug:
        # seed
        from TEMPLATE.db.fixtures import seed_db

        @app.cli.command("seed", help="Seed DB with test data")
        def seed_db_cmd():
            seed_db()

        manager.add_command(seed_db_cmd)

        # init-db
        @app.cli.command(
            "init-db", help="Reinitialize database from scratch (deletes all data)"
        )
        def init_db_cmd():
            db.drop_all(app=app)
            db.create_all(app=app)
            print("Initialized DB")

        manager.add_command(init_db_cmd)

        # config check
        @app.cli.command("config", help="View configuration")
        def config_cmd():
            import pprint

            pprint.pprint(app.config)

        manager.add_command(config_cmd)
