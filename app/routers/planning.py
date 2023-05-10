# System imports
import pymysql

# Libs imports
from fastapi import APIRouter, status, Response, HTTPException

# Local imports
from internal.models import Planning

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/plannings")
async def read_plannings():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning")
        result = cursor.fetchall()
        return result


@router.get("/plannings/{planning_id}")
async def read_planning(planning_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        return {"id": result["id"], "name": result["name"], "id_company": result["id_company"]}


# CREATE
@router.post("/plannings")
async def create_planning(planning: Planning):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE name=%s",
                       (planning.name,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=409, detail="Planning already exists")
        cursor.execute("INSERT INTO planning (name, id_company) VALUES (%s, %s)",
                       (planning.name, planning.id_company,))
        connection.commit()
        return {"id": cursor.lastrowid, "name": planning.name, "id_company": planning.id_company}


# UPDATE
@router.put("/plannings/{planning_id}")
async def update_planning(planning_id: int, planning: Planning):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        cursor.execute("UPDATE planning SET name=%s WHERE id=%s",
                       (planning.name, planning_id))
        connection.commit()
        return {"id": planning_id, "name": planning.name, "id_company": planning.id_company}


# DELETE
@router.delete("/plannings/{planning_id}")
async def delete_planning(planning_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Planning not found")
        cursor.execute("DELETE FROM planning WHERE id=%s", (planning_id,))
        connection.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
