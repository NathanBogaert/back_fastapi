# System imports


# Libs imports
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder

# Local imports
from internal.models import User, right

router = APIRouter()

users = [
    {"id": 1, "name": "John Doe", "email": "johndoe@test.com",
        "right": right.MAINTAINER},
]


@ router.get("/users")
async def get_all_users() -> list[User]:
    if len(users) == 0:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return users


@ router.get("/user/{user_id}")
async def get_user_by_id(user_id: int) -> User:
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found")


@ router.post("/users")
async def create_user(user: User) -> User:
    users.append(user)
    return user
