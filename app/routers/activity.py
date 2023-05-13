# System imports
from typing import Annotated
import pymysql

# Libs imports
from fastapi import APIRouter, status, Depends, HTTPException

# Local imports
from internal.models import Activity
from internal.auth import decode_token

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)


# READ
@router.get("/activities")
async def read_activities(user: Annotated[str, Depends(decode_token)]):
    if user.rights == "MAINTAINER":
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM activity")
            result = cursor.fetchall()
            return result
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT activity.id, activity.name, activity.startTime, activity.endTime, activity.created_by, activity.id_planning FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE planning.id_company=%s", (user.id_company,))
            result = cursor.fetchall()
            return result


@router.get("/activities/{activity_id}")
async def read_activity(activity_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        if user.rights != "MAINTAINER":
            cursor.execute(
                "SELECT * FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE activity.id=%s", (activity_id,))
            id_company_result = cursor.fetchone()
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this activity")
        return {"id": result["id"], "name": result["name"], "startTime": result["startTime"], "endTime": result["endTime"],
                "created_by": result["created_by"], "id_planning": result["id_planning"]}


# TODO: Add a route to get all activities from a planning
@router.get("/activities/planning/{planning_id}")
async def read_activities_from_planning(planning_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        if user.rights != "MAINTAINER":
            # Verify if user is in the same company as the planning
            if user.id_company != result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this planning")
        cursor.execute(
            "SELECT * FROM activity WHERE id_planning=%s", (planning_id,))
        result = cursor.fetchall()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No activities found for this planning")
        return result


# CREATE
@router.post("/activities")
async def create_activity(activity: Activity, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s",
                       (activity.id_planning,))
        id_company_result = cursor.fetchone()
        if not id_company_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        # Verify if user is in the same company as the planning
        if user.rights != "MAINTAINER" and user.id_company != id_company_result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You can't create an activity for a planning that is not in your company")
        cursor.execute("INSERT INTO activity (name, startTime, endTime, created_by, id_planning) VALUES (%s, %s, %s, %s, %s)",
                       (activity.name, activity.startTime, activity.endTime, user.id, activity.id_planning,))
        connection.commit()
        return {"id": activity.id, "name": activity.name, "startTime": activity.startTime, "endTime": activity.endTime,
                "created_by": user.id, "id_planning": activity.id_planning}


# UPDATE
@router.put("/activities/{activity_id}")
async def update_activity(activity_id: int, activity: Activity, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        if user.rights == "USER" or user.rights == "ADMIN":
            if user.rights == "USER":
                # Verify if user is the creator of the activity
                if user.id != result["created_by"]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="You can't update an activity that you didn't create")
            cursor.execute("SELECT * FROM planning WHERE id=%s",
                           (activity.id_planning,))
            id_company_result = cursor.fetchone()
            # Verify if the planning was deleted since the activity was created
            if not id_company_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="The planning of this activity was deleted")
            # Verify if the planning was moved to another company since the activity was created
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="The planning of this activity was moved to another company")
        cursor.execute("UPDATE activity SET name=%s, startTime=%s, endTime=%s, created_by=%s, id_planning=%s WHERE id=%s",
                       (activity.name, activity.startTime, activity.endTime, result["created_by"], activity.id_planning, activity_id,))
        connection.commit()
        return {"id": activity_id, "name": activity.name, "startTime": activity.startTime, "endTime": activity.endTime,
                "created_by": result["created_by"], "id_planning": activity.id_planning}


# DELETE
@router.delete("/activities/{activity_id}")
async def delete_activity(activity_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        if user.rights != "MAINTAINER":
            cursor.execute(
                "SELECT * FROM planning WHERE id=%s", (result["id_planning"],))
            id_company_result = cursor.fetchone()
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete an activity that is not in your company")
        cursor.execute("DELETE FROM activity WHERE id=%s", (activity_id,))
        connection.commit()
        return {"message": "Activity deleted"}
