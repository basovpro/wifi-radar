from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, DateTime, func # type: ignore
from geoalchemy2 import Geography # type: ignore
from .db import Base

class Hotspot(Base):
    __tablename__ = "hotspots"

    id = Column(Integer, primary_key=True)
    bssid = Column(String(17), unique=True, nullable=False)  # AA:BB:CC:DD:EE:FF
    ssid = Column(String, nullable=True)
    geom = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())

class Ping(Base):
    __tablename__ = "pings"

    id = Column(Integer, primary_key=True)
    hotspot_id = Column(Integer, nullable=False)
    internet = Column(Boolean, nullable=False)
    rssi = Column(SmallInteger, nullable=False)
    measured_at = Column(DateTime(timezone=True), server_default=func.now())
