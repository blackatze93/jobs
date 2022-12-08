from typing import List, Optional

from pydantic import BaseModel, Json, EmailStr
import uuid

from pydantic.fields import Dict


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    years_previous_experience: int
    skills: List[Dict[str, int]]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: uuid.UUID





