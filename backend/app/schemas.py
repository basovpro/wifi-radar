from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# -------- входящая схема /ping ------------------------------------------------
class PingIn(BaseModel):
    device_id: str                          # UUID строки (пока как str)
    bssid: str                              # "AA:BB:CC:DD:EE:FF"
    internet: bool
    rssi: int = Field(..., ge=-100, le=0)   # -100…0 dBm
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lon: Optional[float] = Field(None, ge=-180, le=180)
    measured_at: datetime

    class Config:
        orm_mode = True        # Pydantic v1; если уже v2 — use 'from_attributes = True'


# -------- исходящая схема /points --------------------------------------------
class PointOut(BaseModel):
    id: int
    bssid: str
    ssid: Optional[str] = None
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    internet: bool
    rssi: int
    measured_at: datetime

    class Config:
        orm_mode = True        # или_
