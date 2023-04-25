# System imports
from enum import Enum

# Libs imports
from pydantic import BaseModel

# Local imports


class User(BaseModel):
    id: int
    name: str
    email: str
    right: Enum


class right(Enum):
    MAINTAINER = 1
    ADMIN = 2
    USER = 3


class Company(BaseModel):
    id: int
    name: str
    users: list[User]


class Planning(BaseModel):
    id: int
    name: str
    company: Company
