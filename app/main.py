import uuid
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"msg": "Hello World"}


# Users Endpoints
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: uuid.UUID, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)


# Companies Endpoints
@app.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies


@app.get("/companies/{company_id}", response_model=schemas.Company)
def read_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company


@app.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = crud.get_company_by_email(db, email=company.email)
    if db_company:
        raise HTTPException(status_code=400, detail="Company already registered")
    return crud.create_company(db=db, company=company)


@app.put("/companies/{company_id}", response_model=schemas.Company)
def update_company(company_id: uuid.UUID, company: schemas.CompanyUpdate, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.update_company(db=db, company_id=company_id, company=company)


@app.delete("/companies/{company_id}", response_model=schemas.Company)
def delete_company(company_id: uuid.UUID, db: Session = Depends(get_db)):
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.delete_company(db=db, company_id=company_id)


# Vacancies Endpoints
@app.get("/vacancies/", response_model=List[schemas.Vacancy])
def read_vacancies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vacancies = crud.get_vacancies(db, skip=skip, limit=limit)
    return vacancies


@app.get("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def read_vacancy(vacancy_id: uuid.UUID, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return db_vacancy


@app.post("/companies/{company_id}/vacancies/", response_model=schemas.Vacancy)
def create_vacancy(company_id: uuid.UUID, vacancy: schemas.VacancyCreate, db: Session = Depends(get_db)):
    return crud.create_vacancy(db=db, vacancy=vacancy, company_id=company_id)


@app.put("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def update_vacancy(vacancy_id: uuid.UUID, vacancy: schemas.VacancyUpdate, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return crud.update_vacancy(db=db, vacancy_id=vacancy_id, vacancy=vacancy)


@app.delete("/vacancies/{vacancy_id}", response_model=schemas.Vacancy)
def delete_vacancy(vacancy_id: uuid.UUID, db: Session = Depends(get_db)):
    db_vacancy = crud.get_vacancy(db, vacancy_id=vacancy_id)
    if db_vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return crud.delete_vacancy(db=db, vacancy_id=vacancy_id)


@app.get("/search_vacancies/")
def search_vacancies(
        query: str = Query(
            title="Query",
            description="Search query",
            example="python 5 años, sql 3 años, django 2 años"
        ),
        db: Session = Depends(get_db)):
    vacancies = crud.search_vacancies(db, query=query)
    return vacancies