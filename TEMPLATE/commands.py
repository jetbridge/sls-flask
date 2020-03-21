"""CLI commands."""
from .db import db
import flask_migrate


def drop_all_tables(app):
    if not app.config["DEV_DB_SCRIPTS_ENABLED"]:
        raise Exception("Please don't wipe production DB")
    db.engine.execute("DROP SCHEMA public CASCADE")
    db.engine.execute("CREATE SCHEMA public")


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
            print(f"Initializing {db.engine.url}")
            db.drop_all(app=app)
            db.create_all(app=app)
            print("Initialized DB")

        manager.add_command(init_db_cmd)

        @app.cli.command("drop-db", help="Drop every table in the database")
        def drop_db_cmd():
            print(f"Dropping all tables in {db.engine.url}")
            db.reflect(app=app)
            db.drop_all(app=app)
            print("Success")

        manager.add_command(drop_db_cmd)

        # config check
        @app.cli.command("config", help="View configuration")
        def config_cmd():
            import pprint

            pprint.pprint(app.config)

        manager.add_command(config_cmd)


def init_handler(event, context):
    from TEMPLATE.app import app

    if not app.config.get("DEV_DB_SCRIPTS_ENABLED"):
        raise Exception("DEV_DB_SCRIPTS_ENABLED is not enabled")
    with app.app_context():
        drop_all_tables(app=app)
        db.create_all(app=app)
    return "DB initialized."


def seed_handler(event, context):
    """Lambda entry point."""
    from TEMPLATE.app import app

    if not app.config.get("DEV_DB_SCRIPTS_ENABLED"):
        raise Exception("DEV_DB_SCRIPTS_ENABLED is not enabled")

    from TEMPLATE.db.fixtures import seed_db

    with app.app_context():
        seed_db()

    return "Seeded DB."


def migrate_handler(event, context):
    from TEMPLATE.app import app

    with app.app_context():
        flask_migrate.upgrade()
    return "Migrated"
