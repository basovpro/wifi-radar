from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from datetime import datetime

def create_ping(db: Session, p: schemas.PingIn):
    # 1. найдём/создадим хот-спот
    hotspot = (
        db.query(models.Hotspot)
        .filter(models.Hotspot.bssid == p.bssid)
        .first()
    )
    if hotspot is None and p.lat is not None and p.lon is not None:
        hotspot = models.Hotspot(
            bssid=p.bssid,
            ssid=None,
            geom=from_shape(Point(p.lon, p.lat), srid=4326),
            first_seen=p.measured_at,
            last_seen=p.measured_at,
        )
        db.add(hotspot)
        db.flush()        # получаем hotspot.id

    # 2. записываем пинг
    db.add(
        models.Ping(
            hotspot_id=hotspot.id if hotspot else None,
            internet=p.internet,
            rssi=p.rssi,
            measured_at=p.measured_at,
        )
    )
    db.commit()
