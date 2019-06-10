from TEMPLATE.db.fixtures import DEFAULT_PASSWORD


def test_login(client_unauthenticated, user, db_session):
    response = client_unauthenticated.post(
        "/api/auth/login", json=dict(email=user.email, password=DEFAULT_PASSWORD)
    )
    assert response.status_code == 200
    assert response.json.get("access_token")
    assert response.json.get("refresh_token")

    # attempt refresh
    refresh_token = response.json.get("refresh_token")
    response = client_unauthenticated.post(
        "/api/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    ).json
    access_token = response.get("access_token")

    # test new token
    response = client_unauthenticated.get(
        "/api/auth/check", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
