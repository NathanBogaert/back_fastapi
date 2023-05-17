# System imports
from typing import Annotated
import pymysql
import hashlib

# Libs imports
from fastapi import APIRouter, status, HTTPException, Depends
from cryptography.fernet import Fernet

# Local imports
from internal.models import User
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
@router.get("/users")
async def read_users(user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    if user.rights == "ADMIN":
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user.`id`, user.`username`, user.`firstname`, user.`lastname`, user.`email`, user.`rights`, company.`name` FROM user INNER JOIN company ON user.id_company = company.id WHERE user.id_company=%s", (user.id_company,))
            result = cursor.fetchall()
            for user in result:
                user["firstname"] = f.decrypt(user["firstname"].encode())
                user["lastname"] = f.decrypt(user["lastname"].encode())
                user["email"] = f.decrypt(user["email"].encode())
            return result
    if user.rights == "MAINTAINER":
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user.`id`, user.`username`, user.`firstname`, user.`lastname`, user.`email`, user.`rights`, company.`name` FROM user INNER JOIN company ON user.id_company = company.id")
            result = cursor.fetchall()
            for user in result:
                user["firstname"] = f.decrypt(user["firstname"].encode())
                user["lastname"] = f.decrypt(user["lastname"].encode())
                user["email"] = f.decrypt(user["email"].encode())
            return result


@router.get("/users/{user_id}")
async def read_user(user_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT user.`id`, user.`username`, user.`firstname`, user.`lastname`, user.`email`, user.`rights`, user.`id_company`, company.`name` AS company_name FROM user INNER JOIN company ON user.id_company = company.id WHERE user.id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Verify if user is in the same company as the user he wants to see
        if user.id_company != result["id_company"] and user.rights != "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this ressource.",
            )
        return {"id": result["id"], "username": result["username"], "firstname": f.decrypt(result["firstname"].encode()),
                "lastname": f.decrypt(result["lastname"].encode()), "email": f.decrypt(result["email"].encode()),
                "rights": result["rights"], "company name": result["company_name"]}


@router.get("/users/company/{company_id}")
async def read_company_users(company_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company WHERE id=%s", (company_id,))
        company = cursor.fetchone()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
        cursor.execute(
            "SELECT user.`id`, user.`username`, user.`firstname`, user.`lastname`, user.`email`, user.`rights`, company.`name` FROM user INNER JOIN company ON user.id_company = company.id WHERE user.id_company=%s", (company_id,))
        result = cursor.fetchall()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No user found for this company")
        for user in result:
            user["firstname"] = f.decrypt(user["firstname"].encode())
            user["lastname"] = f.decrypt(user["lastname"].encode())
            user["email"] = f.decrypt(user["email"].encode())
        return result


# CREATE
@router.post("/users")
async def create_user(user_create: User,  user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        # Verify if all fields are filled
        if user_create.username == "" or user_create.firstname == "" or user_create.lastname == "" or user_create.password == "" or user_create.email == "" or user_create.rights == "" or user_create.id_company == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing fields")
        cursor.execute("SELECT * FROM user WHERE username=%s",
                       (user_create.username,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        cursor.execute("INSERT INTO user (username, firstname, lastname, password, email, rights, id_company) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (user_create.username, f.encrypt(user_create.firstname.encode()), f.encrypt(user_create.lastname.encode()),
                        hashlib.sha256(user_create.password.encode()).hexdigest(
                       ), f.encrypt(user_create.email.encode()),
                           user_create.rights, user_create.id_company))
        connection.commit()
        return {"id": user_create.id, "username": user_create.username, "firstname": user_create.firstname, "lastname": user_create.lastname,
                "email": user_create.email, "rights": user_create.rights, "id_company": user_create.id_company}


# UPDATE
@router.put("/users/{user_id}")
async def update_user(user_id: int, user_update: User, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Verify if all fields are filled
        if user_update.username == "":
            user_update.username = result["username"]
        if user_update.firstname == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing firstname")
        if user_update.lastname == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing lastname")
        if user_update.password == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing password")
        if user_update.email == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Missing email")
        if user_update.rights == "":
            user_update.rights = result["rights"]
        if user_update.id_company == 0:
            user_update.id_company = result["id_company"]
        # Verify if user is in the same company as the user he wants to modify
        if user.id_company != result["id_company"] and user.rights != "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this ressource.",
            )
        # Verify if the user is trying to change the company to another company
        if user.rights != "MAINTAINER" and user.id_company != user_update.id_company:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to modify the company of this user.",
            )
        # Verify if user is trying to change a maintainer
        if user.rights != "MAINTAINER" and result["rights"] == "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't modify a maintainer.",
            )
        # Verify if user is trying to change a user to maintainer
        if user.rights != "MAINTAINER" and user_update.rights == "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't modify rights to maintainer.",
            )
        if result["id"] != user_id:
            if user_update.username == result["username"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="This username is already taken")
        cursor.execute("UPDATE user SET username=%s, firstname=%s, lastname=%s, password=%s, email=%s, rights=%s, id_company=%s WHERE id=%s",
                       (user_update.username, f.encrypt(user_update.firstname.encode()), f.encrypt(user_update.lastname.encode()),
                        hashlib.sha256(user_update.password.encode()).hexdigest(
                       ), f.encrypt(user_update.email.encode()),
                           user_update.rights, user_update.id_company, user_id))
        connection.commit()
        return {"id": user_id, "username": user_update.username, "firstname": user_update.firstname, "lastname": user_update.lastname,
                "email": user_update.email, "rights": user_update.rights, "id_company": user_update.id_company}


# DELETE
@router.delete("/users/{user_id}")
async def delete_user(user_id: int, user: Annotated[str, Depends(decode_token)]):
    if user.rights != "MAINTAINER" and user.rights != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this ressource.",
        )
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        # Verify if user is in the same company as the user he wants to delete
        if user.id_company != result["id_company"] and user.rights != "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't delete user from another company.",
            )
        # Verify if user is trying to delete a maintainer
        if user.rights != "MAINTAINER" and result["rights"] == "MAINTAINER":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't delete a maintainer.",
            )
        cursor.execute("DELETE FROM user WHERE id=%s", (user_id,))
        connection.commit()
        return {"message": "User deleted"}
