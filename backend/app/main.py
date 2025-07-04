from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import deps, schemas, crud

app = FastAPI()


# ───────── системный энд-пойнт ─────────
@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# ───────── приём данных сканирования ────
@app.post("/ping", status_code=201)
def ping(
    p: schemas.PingIn,
    db: Session = Depends(deps.get_db),
) -> dict[str, int]:
    try:
        crud.create_ping(db, p)
    except Exception:
        # здесь можно добавить логирование stacktrace
        raise HTTPException(status_code=500, detail="db error")
    return {"saved": 1}


# ───────── отдача точек Wi-Fi рядом ─────
@app.get("/points", response_model=list[schemas.PointOut])
def points(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius: int = Query(300, ge=50, le=2000, description="радиус, м"),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(deps.get_db),
) -> list[schemas.PointOut]:
    """
    Вернуть хот-споты с рабочим интернетом в радиусе ``radius`` м
    вокруг координаты ``[lat, lon]``, не более ``limit`` штук.
    """
    try:
        return crud.get_points(db, lat, lon, radius, limit)
    except Exception:
        raise HTTPException(status_code=500, detail="query error")
