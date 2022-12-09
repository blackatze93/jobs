from typing import List, Optional

from pydantic import BaseModel, Json, EmailStr, root_validator, AnyUrl, AnyHttpUrl
import uuid

from pydantic.fields import Dict, Field


# User Schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    years_previous_experience: int
    skills: List[Dict[str, int]] = Field(example=[{"python": 5}, {"sql": 3}])

    @root_validator(pre=True)
    def validate_skills(cls, values):
        if values.get("skills"):
            if not isinstance(values.get('skills'), list):
                raise ValueError('skills must be a list')
            for skill in values.get('skills'):
                if not isinstance(skill, dict):
                    raise ValueError('skills must be a list of dicts')
                if len(skill) != 1:
                    raise ValueError('skills must be a list of dicts with one key')
        return values

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    first_name: str = None
    last_name: str = None
    email: EmailStr = None
    years_previous_experience: int = None
    skills: List[Dict[str, int]] = None


class User(UserBase):
    id: uuid.UUID


# Vacancy Schemas
class VacancyBase(BaseModel):
    position_name: str
    salary: int
    currency: str
    link: AnyHttpUrl
    required_skills: List[Dict[str, int]] = Field(example=[{"python": 5}, {"sql": 3}])

    @root_validator(pre=True)
    def validate_skills(cls, values):
        if values.get("required_skills"):
            if not isinstance(values.get('required_skills'), list):
                raise ValueError('required_skills must be a list')
            for skill in values.get('required_skills'):
                if not isinstance(skill, dict):
                    raise ValueError('required_skills must be a list of dicts')
                if len(skill) != 1:
                    raise ValueError('required_skills must be a list of dicts with one key')
        return values

    class Config:
        orm_mode = True


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(VacancyBase):
    position_name: str = None
    salary: int = None
    currency: str = None
    link: AnyHttpUrl = None
    required_skills: List[Dict[str, int]] = None


class Vacancy(VacancyBase):
    id: uuid.UUID
    company_id: uuid.UUID


# Company Schemas
class CompanyBase(BaseModel):
    name: str
    email: EmailStr
    website: AnyHttpUrl

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    name: str = None
    email: EmailStr = None
    website: AnyHttpUrl = None


class Company(CompanyBase):
    id: uuid.UUID
    vacancies: List[Vacancy] = []
