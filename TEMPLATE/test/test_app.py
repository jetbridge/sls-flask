from TEMPLATE.create_app import create_app
from TEMPLATE.config import check_valid


def test_config():
    app = create_app(dict(TESTING=True))
    assert check_valid(app.config), "app config check failed"


def test_db(db_session):
    assert db_session.execute('SELECT 1').scalar() == 1, "test DB query failed"
