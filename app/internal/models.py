# System imports
from enum import Enum

# Libs imports
from pydantic import BaseModel

# Local imports


class Company(BaseModel):
    id: int
    name: str


class User(BaseModel):
    id: int
    name: str
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
    startTime: str
    endTime: str
    id_planning: int
