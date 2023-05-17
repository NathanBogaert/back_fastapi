# System imports
from datetime import datetime

# Libs imports
from pydantic import BaseModel

# Local imports


class Company(BaseModel):
    id: int
    name: str = ""


class User(BaseModel):
    id: int
    username: str = ""
    firstname: str = ""
    lastname: str = ""
    password: str = ""
    email: str = ""
    rights: str = ""
    id_company: int = 0


class Planning(BaseModel):
    id: int
    name: str = ""
    id_company: int = 0


class Activity(BaseModel):
    id: int
    name: str = ""
    startTime: datetime
    endTime: datetime
    created_by: int = 0
    id_planning: int = 0


class Participant(BaseModel):
    id_user: int
    id_activity: int
