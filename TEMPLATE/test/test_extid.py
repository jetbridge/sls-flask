from TEMPLATE.model import User


def test_can_get_by_extid(user):
    assert User.get_by_extid(user.extid) is not None
