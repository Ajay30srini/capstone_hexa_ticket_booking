def test_register_success(client):
    r = client.post("/auth/register", json={"email": "a@test.com", "password": "abc123", "role": "customer"})
    assert r.status_code in (200, 201), r.text


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@test.com", "password": "abc123", "role": "customer"})
    r2 = client.post("/auth/register", json={"email": "dup@test.com", "password": "abc123", "role": "customer"})
    assert r2.status_code == 400, r2.text


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@test.com", "password": "abc123", "role": "customer"})
    r = client.post("/auth/login", json={"email": "login@test.com", "password": "abc123"})
    assert r.status_code == 200, r.text
    data = r.json()
    assert ("access_token" in data) or ("token" in data)


def test_login_invalid_password(client):
    client.post("/auth/register", json={"email": "bad@test.com", "password": "abc123", "role": "customer"})
    r = client.post("/auth/login", json={"email": "bad@test.com", "password": "wrong"})
    assert r.status_code == 400, r.text