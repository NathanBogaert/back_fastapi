# System imports
from typing import Annotated
import pymysql
from datetime import datetime

# Libs imports
from fastapi import APIRouter, status, Depends, HTTPException
from cryptography.fernet import Fernet

# Local imports
from internal.models import Activity, Participant
from internal.auth import decode_token

router = APIRouter()

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)

key = "JWkLd3kOabKBPLSkqEWXLisyOzP5ejfL3JtML1a21nA="
f = Fernet(key)


# READ
@router.get("/activities")
async def read_activities(user: Annotated[str, Depends(decode_token)]):
    if user.rights == "MAINTAINER":
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT activity.id, activity.name, activity.startTime, activity.endTime, user.firstname AS created_by_user_firstname, user.lastname AS created_by_user_lastname, planning.name, (SELECT COUNT(id_user) FROM participant WHERE id_activity = activity.id) AS participant_count FROM activity INNER JOIN planning ON activity.id_planning=planning.id INNER JOIN user ON activity.created_by=user.id")
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
            for i in result:
                i["created_by_user_firstname"] = f.decrypt(
                    i["created_by_user_firstname"].encode())
                i["created_by_user_lastname"] = f.decrypt(
                    i["created_by_user_lastname"].encode())
            return result
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT activity.id, activity.name, activity.startTime, activity.endTime, user.firstname AS created_by_user_firstname, user.lastname AS created_by_user_lastname, planning.name, (SELECT COUNT(id_user) FROM participant WHERE id_activity = activity.id) AS participant_count FROM activity INNER JOIN planning ON activity.id_planning=planning.id INNER JOIN user ON activity.created_by=user.id WHERE planning.id_company=%s", (user.id_company,))
            result = cursor.fetchall()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
            for i in result:
                i["created_by_user_firstname"] = f.decrypt(
                    i["created_by_user_firstname"].encode())
                i["created_by_user_lastname"] = f.decrypt(
                    i["created_by_user_lastname"].encode())
            return result


@router.get("/activities/{activity_id}")
async def read_activity(activity_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT activity.id, activity.name, activity.startTime, activity.endTime, user.firstname AS created_by_user_firstname, user.lastname AS created_by_user_lastname, planning.name AS planning_name, (SELECT COUNT(id_user) FROM participant WHERE id_activity = activity.id) AS participant_count FROM activity INNER JOIN planning ON activity.id_planning=planning.id INNER JOIN user ON activity.created_by=user.id WHERE activity.id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        if user.rights != "MAINTAINER":
            cursor.execute(
                "SELECT * FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE activity.id=%s", (activity_id,))
            id_company_result = cursor.fetchone()
            if not id_company_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this activity")
        result["created_by_user_firstname"] = f.decrypt(
            result["created_by_user_firstname"].encode())
        result["created_by_user_lastname"] = f.decrypt(
            result["created_by_user_lastname"].encode())
        return result


@router.get("/activities/planning/{planning_id}")
async def read_activities_from_planning(planning_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM planning WHERE id=%s", (planning_id,))
        id_planning_result = cursor.fetchone()
        if not id_planning_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        if user.rights != "MAINTAINER":
            # Verify if user is in the same company as the planning
            if user.id_company != id_planning_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this planning")
        cursor.execute(
            "SELECT activity.id, activity.name, activity.startTime, activity.endTime, user.firstname AS created_by_user_firstname, user.lastname AS created_by_user_lastname, planning.name AS planning_name, (SELECT COUNT(id_user) FROM participant WHERE id_activity = activity.id) AS participant_count FROM activity INNER JOIN planning ON activity.id_planning=planning.id INNER JOIN user ON activity.created_by=user.id WHERE id_planning=%s", (planning_id,))
        result = cursor.fetchall()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No activities found for this planning")
        for i in result:
            i["created_by_user_firstname"] = f.decrypt(
                i["created_by_user_firstname"].encode())
            i["created_by_user_lastname"] = f.decrypt(
                i["created_by_user_lastname"].encode())
        return result


@router.get("/activities/{activity_id}/participants")
async def read_participants_from_activity(activity_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        if user.rights != "MAINTAINER" and user.rights != "ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this resource")
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        id_activity_result = cursor.fetchone()
        if not id_activity_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        if user.rights != "MAINTAINER":
            cursor.execute(
                "SELECT * FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE activity.id=%s", (activity_id,))
            id_company_result = cursor.fetchone()
            if not id_company_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this activity")
        cursor.execute(
            "SELECT user.firstname, user.lastname FROM user INNER JOIN participant ON participant.id_user = user.id WHERE participant.id_activity=%s", (activity_id,))
        result = cursor.fetchall()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No participants found for this activity")
        for user in result:
            user["firstname"] = f.decrypt(user["firstname"].encode())
            user["lastname"] = f.decrypt(user["lastname"].encode())
        return result


# CREATE
@router.post("/activities")
async def create_activity(activity: Activity, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        # Verify if fields are not empty
        if activity.name == "" or activity.id_planning == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")
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


@router.post("/activities/{activity_id}/participants")
async def registration_to_activity(activity_id: int, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM participant WHERE id_activity=%s AND id_user=%s", (activity_id, user.id,))
        participant_result = cursor.fetchone()
        if participant_result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="You are already registered to this activity")
        cursor.execute(
            "SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        cursor.execute(
            "SELECT * FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE activity.id=%s", (activity_id,))
        id_company_result = cursor.fetchone()
        if not id_company_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        # Verify if user is in the same company as the activity
        if user.id_company != id_company_result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You can't participate to an activity that is not in your company")
        cursor.execute("INSERT INTO participant (id_activity, id_user) VALUES (%s, %s)",
                       (activity_id, user.id,))
        connection.commit()
        return {"id_activity": activity_id, "id_user": user.id}


@router.post("/activities/{activity_id}/participants/{user_id}")
async def add_participant_to_activity(activity_id: int, user_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource")
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM participant WHERE id_activity=%s AND id_user=%s", (activity_id, user_id,))
        participant_result = cursor.fetchone()
        if participant_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already registered to this activity")
        cursor.execute(
            "SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        cursor.execute(
            "SELECT * FROM activity INNER JOIN planning ON activity.id_planning=planning.id WHERE activity.id=%s", (activity_id,))
        id_company_result = cursor.fetchone()
        if not id_company_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        id_user_result = cursor.fetchone()
        if not id_user_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Verify if user to add is in the same company as the planning of the activity
        if id_company_result["id_company"] != id_user_result["id_company"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is not in the same company as the activity")
        if user.rights != "MAINTAINER":
            # Verify if user is in the same company as the planning of the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You can't add a participant to an activity that is not in your company")
        cursor.execute("INSERT INTO participant (id_activity, id_user) VALUES (%s, %s)",
                       (activity_id, user_id,))
        connection.commit()
        return {"id_activity": activity_id, "id_user": user_id}


# UPDATE
@router.put("/activities/{activity_id}")
async def update_activity(activity_id: int, activity: Activity, user: Annotated[str, Depends(decode_token)]):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        # Verify if fields are empty
        if activity.name == "":
            activity.name = result["name"]
        if activity.startTime == "":
            activity.startTime = result["startTime"]
        if activity.endTime == "":
            activity.endTime = result["endTime"]
        if activity.id_planning == 0:
            activity.id_planning = result["id_planning"]
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
            if not id_company_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete an activity that is not in your company")
        cursor.execute("DELETE FROM activity WHERE id=%s", (activity_id,))
        connection.commit()
        return {"message": "Activity deleted"}


@router.delete("/activities/{activity_id}/participants/{user_id}")
async def delete_participant_from_activity(activity_id: int, user_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this ressource.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM activity WHERE id=%s", (activity_id,))
        activity_result = cursor.fetchone()
        if not activity_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        cursor.execute(
            "SELECT * FROM participant WHERE id_activity=%s AND id_user=%s", (activity_id, user_id,))
        participant_result = cursor.fetchone()
        if not participant_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Participant not found")
        if user.rights != "MAINTAINER":
            cursor.execute(
                "SELECT * FROM planning WHERE id=%s", (activity_result["id_planning"],))
            id_company_result = cursor.fetchone()
            if not id_company_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Planning not found")
            # Verify if user is in the same company as the activity
            if user.id_company != id_company_result["id_company"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete a participant from an activity that is not in your company")
        cursor.execute("DELETE FROM participant WHERE id_activity=%s AND id_user=%s",
                       (activity_id, user_id,))
        connection.commit()
        return {"message": "Participant deleted from activity"}
