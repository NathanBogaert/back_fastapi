# System imports
from typing import Annotated
import pymysql

# Libs imports
from fastapi import APIRouter, status, Depends, HTTPException

# Local imports
from internal.models import Planning
from internal.auth import decode_token

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/plannings")
async def read_plannings(user: Annotated[str, Depends(decode_token)]):
    if user.rights == "MAINTAINER":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM planning")
            result = cursor.fetchall()
            return result
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM planning WHERE id_company=%s", (user.id_company,))
            result = cursor.fetchall()
            return result


@router.get("/plannings/{planning_id}")
async def read_planning(planning_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=403, detail="You don't have access to this planning")
        return {"id": result["id"], "name": result["name"], "id_company": result["id_company"]}


# CREATE
@router.post("/plannings")
async def create_planning(planning: Planning, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        if user.rights != "MAINTAINER" and user.id_company != planning.id_company:
            raise HTTPException(
                status_code=403, detail="You don't have access to this ressource.")
        cursor.execute("INSERT INTO planning (name, id_company) VALUES (%s, %s)",
                       (planning.name, planning.id_company,))
        connection.commit()
        return {"id": planning.id, "name": planning.name, "id_company": planning.id_company}


# UPDATE
@router.put("/plannings/{planning_id}")
async def update_planning(planning_id: int, planning: Planning, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=403, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=403, detail="You don't have access to this planning")
        if user.rights != "MAINTAINER" and user.id_company != planning.id_company:
            raise HTTPException(
                status_code=403, detail="You can't change the company of this planning")
        cursor.execute("UPDATE planning SET name=%s, id_company=%s WHERE id=%s",
                       (planning.name, planning.id_company, planning_id))
        connection.commit()
        return {"id": planning_id, "name": planning.name, "id_company": planning.id_company}


# DELETE
@router.delete("/plannings/{planning_id}")
async def delete_planning(planning_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=403, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this ressource.",
            )
        cursor.execute("DELETE FROM planning WHERE id=%s", (planning_id,))
        connection.commit()
        return {"message": "Planning deleted"}
