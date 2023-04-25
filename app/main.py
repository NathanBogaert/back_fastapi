# System imports


# Libs imports
from fastapi import FastAPI, Response, status

# Local imports
from routers import user, company, planning
# from internal import auth

app = FastAPI()


app.include_router(user.router, tags=["User"])
app.include_router(company.router, tags=["Company"])
app.include_router(planning.router, tags=["Planning"])
# app.include_router(auth.router, tags=["Auth"])
