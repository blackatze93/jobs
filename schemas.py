from typing import List, Optional

from pydantic import BaseModel, Json, EmailStr, root_validator
import uuid

from pydantic.fields import Dict, Field


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





