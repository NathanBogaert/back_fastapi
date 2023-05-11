# System imports
import pymysql
import hashlib

# Libs imports
from fastapi import APIRouter, status, Response, HTTPException, Depends
from cryptography.fernet import Fernet

# Local imports
from internal.models import User

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
@ router.get("/users")
async def read_users():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()
        for user in result:
            user["name"] = f.decrypt(user["name"].encode())
            user["email"] = f.decrypt(user["email"].encode())
        return result


@ router.get("/users/{user_id}")
async def read_user(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return {"id": result["id"], "name": f.decrypt(result["name"].encode()), "password": result["password"],
                "email": f.decrypt(result["email"].encode()), "rights": result["rights"], "id_company": result["id_company"]}


# CREATE
@ router.post("/users")
async def create_user(user: User):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE email=%s", (user.email,))
        result = cursor.fetchone()
        if result:
            raise HTTPException(
                status_code=409, detail="User already exists")
        cursor.execute("INSERT INTO user (name, password, email, rights, id_company) VALUES (%s, %s, %s, %s, %s)",
                       (f.encrypt(user.name.encode()), hashlib.sha256(user.password.encode()).hexdigest(),
                        f.encrypt(user.email.encode()), user.rights, user.id_company))
        connection.commit()
        return {"id": cursor.lastrowid, "name": user.name, "password": user.password,
                "email": user.email, "rights": user.rights, "id_company": user.id_company}


# UPDATE
@ router.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        cursor.execute("UPDATE user SET name=%s, password=%s, email=%s, rights=%s, id_company=%s WHERE id=%s",
                       (f.encrypt(user.name.encode()), hashlib.sha256(user.password.encode()).hexdigest(),
                        f.encrypt(user.email.encode()), user.rights, user.id_company, user_id))
        connection.commit()
        return {"id": user_id, "name": user.name, "password": user.password, "email": user.email, "rights": user.rights, "id_company": user.id_company}


# DELETE
@ router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE id=%s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        cursor.execute("DELETE FROM user WHERE id=%s", (user_id,))
        connection.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
