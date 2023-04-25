# System imports


# Libs imports
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder

# Local imports
from internal.models import Company
from routers.user import users

router = APIRouter()

companies = [
    {"id": 1, "name": "Company 1", "users": users}
]


@router.get("/companies")
async def get_all_companies() -> list[Company]:
    if len(companies) == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return companies


@router.get("/company/{company_id}")
async def get_company_by_id(company_id: int) -> Company:
    for company in companies:
        if company["id"] == company_id:
            return company
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Company not found")


@router.post("/companies")
async def create_company(company: Company) -> Company:
    companies.append(company)
    return company
