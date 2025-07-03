from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import deps, schemas, crud

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ping", status_code=201)
def ping(p: schemas.PingIn, db: Session = Depends(deps.get_db)):
    try:
        crud.create_ping(db, p)
    except Exception as e:
        # можно логировать e
        raise HTTPException(status_code=500, detail="db error")
    return {"saved": 1}
