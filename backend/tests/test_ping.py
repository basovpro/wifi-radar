import uuid
from datetime import datetime, timezone


def make_payload(**override):
    data = {
        "device_id": str(uuid.uuid4()),
        "bssid": "AA:BB:CC:DD:EE:FF",
        "internet": True,
        "rssi": -42,
        "lat": 59.93,
        "lon": 30.36,
        "measured_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    data.update(override)
    return data


def test_ping_created(client):
    resp = client.post("/ping", json=make_payload())
    assert resp.status_code == 201
    assert resp.json() == {"saved": 1}


def test_ping_validation_error(client):
    bad = make_payload(rssi=-300)  # недопустимо
    resp = client.post("/ping", json=bad)
    assert resp.status_code == 422
