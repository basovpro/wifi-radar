from typing import List

from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


# ─────────────────────────  /ping  ──────────────────────────
def create_ping(db: Session, p: schemas.PingIn) -> None:
    """Сохранить один пинг и при необходимости создать хот-спот."""
    hotspot = db.query(models.Hotspot).filter(models.Hotspot.bssid == p.bssid).first()

    if hotspot is None and p.lat is not None and p.lon is not None:
        hotspot = models.Hotspot(
            bssid=p.bssid,
            ssid=None,
            geom=from_shape(Point(p.lon, p.lat), srid=4326),
            first_seen=p.measured_at,
            last_seen=p.measured_at,
        )
        db.add(hotspot)
        db.flush()  # получаем hotspot.id

    db.add(
        models.Ping(
            hotspot_id=hotspot.id if hotspot else None,
            internet=p.internet,
            rssi=p.rssi,
            measured_at=p.measured_at,
        )
    )
    db.commit()


# ─────────────────────────  /points  ─────────────────────────
def get_points(
    db: Session,
    lat: float,
    lon: float,
    radius_m: int = 300,
    limit: int = 100,
) -> List[schemas.PointOut]:
    """Вернуть точки Wi-Fi с интернетом в радиусе radius_m (метров)."""
    user_geom_wkt = f"SRID=4326;POINT({lon} {lat})"

    stmt = (
        select(models.Hotspot, models.Ping)
        .join(models.Ping, models.Ping.hotspot_id == models.Hotspot.id)
        .where(
            models.Ping.internet.is_(True),
            ST_DWithin(
                models.Hotspot.geom,
                user_geom_wkt,
                radius_m,
                use_spheroid=True,
            ),
        )
        .order_by(models.Ping.measured_at.desc())
        .limit(limit)
    )

    rows = db.execute(stmt).all()

    result: list[schemas.PointOut] = []
    for hotspot, ping in rows:
        point = to_shape(hotspot.geom)
        result.append(
            schemas.PointOut(
                id=hotspot.id,
                bssid=hotspot.bssid,
                ssid=hotspot.ssid,
                lat=point.y,
                lon=point.x,
                internet=ping.internet,
                rssi=ping.rssi,
                measured_at=ping.measured_at,
            )
        )
    return result
