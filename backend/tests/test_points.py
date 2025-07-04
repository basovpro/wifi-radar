from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_points_validation():
    r = client.get("/points", params={"lat": 100, "lon": 0})
    assert r.status_code == 422
