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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        # Verify if user is in the same company as the planning
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this planning")
        return {"id": result["id"], "name": result["name"], "id_company": result["id_company"]}


# TODO: Add a route to get all plannings from a company
@router.get("/companies/{company_id}/plannings")
async def read_plannings_from_company(company_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        id_company_result = cursor.fetchone()
        if not id_company_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        cursor.execute(
            "SELECT * FROM planning WHERE id_company=%s", (company_id,))
        result = cursor.fetchall()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No plannings found for this company")
        return result


# CREATE
@router.post("/plannings")
async def create_planning(planning: Planning, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        # Verify if user is in the same company as the planning he wants to create
        if user.rights != "MAINTAINER" and user.id_company != planning.id_company:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You can't create a planning for another company")
        cursor.execute("INSERT INTO planning (name, id_company) VALUES (%s, %s)",
                       (planning.name, planning.id_company,))
        connection.commit()
        return {"id": planning.id, "name": planning.name, "id_company": planning.id_company}


# UPDATE
@router.put("/plannings/{planning_id}")
async def update_planning(planning_id: int, planning: Planning, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        # Verify if user is in the same company as the planning he wants to update
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You can't update a planning from another company")
        # Verify if user is trying to change the company of the planning to another company
        if user.rights != "MAINTAINER" and user.id_company != planning.id_company:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You can't change the company of a planning to another company")
        cursor.execute("UPDATE planning SET name=%s, id_company=%s WHERE id=%s",
                       (planning.name, planning.id_company, planning_id))
        connection.commit()
        return {"id": planning_id, "name": planning.name, "id_company": planning.id_company}


# DELETE
@router.delete("/plannings/{planning_id}")
async def delete_planning(planning_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        # Verify if user is in the same company as the planning he wants to delete
        if user.rights != "MAINTAINER" and user.id_company != result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't delete a planning from another company",
            )
        cursor.execute("DELETE FROM planning WHERE id=%s", (planning_id,))
        connection.commit()
        return {"message": "Planning deleted"}
