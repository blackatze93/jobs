from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, EmailType, URLType, JSONType
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(EmailType, unique=True, index=True)
    years_previous_experience = Column(Integer)
    skills = Column(JSONType)


class Company(Base):
    __tablename__ = "companies"
    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(EmailType, unique=True, index=True)
    website = Column(URLType)

    vacancies = relationship("Vacancy", back_populates="company")


class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    position_name = Column(String)
    salary = Column(Integer)
    currency = Column(String)
    link = Column(URLType)
    required_skills = Column(JSONType)

    company_id = Column(UUIDType(binary=False), ForeignKey("companies.id"))
    company = relationship("Company", back_populates="vacancies")



