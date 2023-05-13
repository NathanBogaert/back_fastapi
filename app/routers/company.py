# System imports
from typing import Annotated
import pymysql

# Libs imports
from fastapi import APIRouter, status, Depends, HTTPException

# Local imports
from internal.models import Company
from internal.auth import decode_token

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/companies")
async def read_companies(user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company")
        result = cursor.fetchall()
        return result


@router.get("/companies/{company_id}")
async def read_company(company_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        return {"id": result["id"], "name": result["name"]}


# CREATE
@router.post("/companies")
async def create_company(company: Company, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE name=%s", (company.name,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Company already exists")
        cursor.execute("INSERT INTO company (name) VALUES (%s)",
                       (company.name,))
        connection.commit()
        return {"id": company.id, "name": company.name}


# UPDATE
@router.put("/companies/{company_id}")
async def update_company(company_id: int, company: Company, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        cursor.execute("UPDATE company SET name=%s WHERE id=%s",
                       (company.name, company_id))
        connection.commit()
        return {"id": company_id, "name": company.name}


# DELETE
@router.delete("/companies/{company_id}")
async def delete_company(company_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        cursor.execute("DELETE FROM company WHERE id=%s", (company_id,))
        connection.commit()
        return {"message": "Company deleted"}
