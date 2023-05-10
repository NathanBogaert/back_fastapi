# System imports
import pymysql

# Libs imports
from fastapi import APIRouter, status, Response, HTTPException

# Local imports
from internal.models import Company

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/companies")
async def read_companies():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company")
        result = cursor.fetchall()
        return result


@router.get("/companies/{company_id}")
async def read_company(company_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        return {"id": result["id"], "name": result["name"]}


# CREATE
@router.post("/companies")
async def create_company(company: Company):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE name=%s", (company.name,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=409, detail="Company already exists")
        cursor.execute("INSERT INTO company (name) VALUES (%s)",
                       (company.name,))
        connection.commit()
        return {"id": cursor.lastrowid, "name": company.name}


# UPDATE
@router.put("/companies/{company_id}")
async def update_company(company_id: int, company: Company):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        cursor.execute("UPDATE company SET name=%s WHERE id=%s",
                       (company.name, company_id))
        connection.commit()
        return {"id": company_id, "name": company.name}


# DELETE
@router.delete("/companies/{company_id}")
async def delete_company(company_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Company not found")
        cursor.execute("DELETE FROM company WHERE id=%s", (company_id,))
        connection.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
