import uuid

from sqlalchemy.orm import Session

from . import models, schemas


# Users CRUD
def get_user(db: Session, user_id: uuid.UUID):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: uuid.UUID, user: schemas.UserUpdate):
    db_user = get_user(db, user_id=user_id)
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: uuid.UUID):
    db_user = get_user(db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    return db_user


# Vacancies CRUD
def get_vacancy(db: Session, vacancy_id: uuid.UUID):
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()


def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacancy).offset(skip).limit(limit).all()


def create_vacancy(db: Session, vacancy: schemas.VacancyCreate, company_id: uuid.UUID):
    db_vacancy = models.Vacancy(**vacancy.dict(), company_id=company_id)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


def update_vacancy(db: Session, vacancy_id: uuid.UUID, vacancy: schemas.VacancyUpdate):
    db_vacancy = get_vacancy(db, vacancy_id=vacancy_id)
    for key, value in vacancy.dict(exclude_unset=True).items():
        setattr(db_vacancy, key, value)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy


def delete_vacancy(db: Session, vacancy_id: uuid.UUID):
    db_vacancy = get_vacancy(db, vacancy_id=vacancy_id)
    db.delete(db_vacancy)
    db.commit()
    return db_vacancy



# Companies CRUD
def get_company(db: Session, company_id: uuid.UUID):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_company_by_email(db: Session, email: str):
    return db.query(models.Company).filter(models.Company.email == email).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company_id: uuid.UUID, company: schemas.CompanyUpdate):
    db_company = get_company(db, company_id=company_id)
    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: uuid.UUID):
    db_company = get_company(db, company_id=company_id)
    db.delete(db_company)
    db.commit()
    return db_company
