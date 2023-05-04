# System imports

# Libs imports
import pymysql
from fastapi import APIRouter, status, Response, HTTPException

# Local imports
from internal.models import Activity

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/activities")
async def read_activities():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity")
        result = cursor.fetchall()
        return result


@router.get("/activities/{activity_id}")
async def read_activity(activity_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Activity not found")
        return {"id": result["id"], "name": result["name"], "startTime": result["startTime"], "endTime": result["endTime"], "id_planning": result["id_planning"]}


# CREATE
@router.post("/activities")
async def create_activity(activity: Activity):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE name=%s",
                       (activity.name,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=409, detail="Activity already exists")
        cursor.execute("INSERT INTO activity (name, startTime, endTime, id_planning) VALUES (%s, %s, %s, %s)",
                       (activity.name, activity.startTime, activity.endTime, activity.id_planning,))
        connection.commit()
        return {"id": cursor.lastrowid, "name": activity.name, "startTime": activity.startTime, "endTime": activity.endTime, "id_planning": activity.id_planning}


# UPDATE
@router.put("/activities/{activity_id}")
async def update_activity(activity_id: int, activity: Activity):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Activity not found")
        cursor.execute("UPDATE activity SET name=%s, startTime=%s, endTime=%s, id_planning=%s WHERE id=%s",
                       (activity.name, activity.startTime, activity.endTime, activity.id_planning, activity_id,))
        connection.commit()
        return {"id": activity_id, "name": activity.name, "startTime": activity.startTime, "endTime": activity.endTime, "id_planning": activity.id_planning}


# DELETE
@router.delete("/activities/{activity_id}")
async def delete_activity(activity_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Activity not found")
        cursor.execute("DELETE FROM activity WHERE id=%s", (activity_id,))
        connection.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
