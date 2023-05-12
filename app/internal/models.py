# System imports
from enum import Enum
from datetime import datetime

# Libs imports
from pydantic import BaseModel

# Local imports


class Company(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    password: str
    email: str
    rights: str
    id_company: int


class Planning(BaseModel):
    id: int
    name: str
    id_company: int


class Activity(BaseModel):
    id: int
    name: str
    startTime: datetime
    endTime: datetime
    created_by: int
    id_planning: int
