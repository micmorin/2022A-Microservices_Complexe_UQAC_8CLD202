from fastapi import Depends, FastAPI, Response, Request, Form
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=404)
def main_index(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.main_index(db, response, request)

@app.post("/login", status_code=200)
def main_login(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.main_login(db, response, request)

@app.get("/users/", status_code=200)
def user_index(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.user_index(db, response, request)

@app.post("/users/create", status_code=200)
def user_create(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.user_create(db, response, request)

@app.put("/users/update", status_code=200)
def user_update(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.user_update(db, response, request)

@app.delete("/users/delete", status_code=200)
def user_delete(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.user_delete(db, response, request)

@app.get("/profils/", status_code=200)
def profil_index(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.profil_index(db, response, request)

@app.post("/profils/create", status_code=200)
def profil_create(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.profil_create(db, response, request)

@app.put("/profils/update", status_code=200)
def profil_update(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.profil_update(db, response, request)

@app.delete("/profils/delete", status_code=200)
def profil_delete(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.profil_delete(db, response, request)

@app.post("/calculs/", status_code=200)
def calcul_index(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.calcul_index(db, response, request)

@app.delete("/calculs/delete", status_code=200)
def calcul_delete(request: Request, response: Response, db: Session = Depends(get_db)):
    return crud.calcul_delete(db, response, request)