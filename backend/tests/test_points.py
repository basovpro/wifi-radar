def test_points_empty(client):
    resp = client.get("/points?lat=59.93&lon=30.36")
    assert resp.status_code == 200
    assert resp.json() == []


def test_points_after_ping(client):
    payload = {
        "device_id": "550e8400-e29b-41d4-a716-446655440000",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "internet": True,
        "rssi": -60,
        "lat": 59.9311,
        "lon": 30.3609,
        "measured_at": "2025-07-04T21:00:00Z",
    }
    client.post("/ping", json=payload)

    resp = client.get("/points?lat=59.93&lon=30.36&radius=500")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["bssid"] == "AA:BB:CC:DD:EE:FF"
