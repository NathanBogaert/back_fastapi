# System imports


# Libs imports
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder

# Local imports
from internal.models import Planning
from routers.company import companies

router = APIRouter()

planning = [
    {"id": 1, "name": "Planning 1", "company": companies}
]


@router.get("/plannings")
async def get_all_planning() -> list[Planning]:
    if len(planning) == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return planning


@router.get("/planning/{planning_id}")
async def get_planning_by_id(planning_id: int) -> Planning:
    for plan in planning:
        if plan["id"] == planning_id:
            return plan
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Planning not found")


@router.post("/planning")
async def create_planning(plan: Planning) -> Planning:
    planning.append(plan)
    return plan
