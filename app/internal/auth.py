# System imports
from typing import Annotated
import hashlib
import pymysql

# Libs imports
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from cryptography.fernet import Fernet

# Local imports
from internal.models import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

connection = pymysql.connect(host='host.docker.internal',
                             user='root',
                             password='',
                             database='back-python',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor(pymysql.cursors.DictCursor)

JWT_KEY = "kajshkdalasjjlhgkjguifoudhsfkxahdsf"

key = "JWkLd3kOabKBPLSkqEWXLisyOzP5ejfL3JtML1a21nA="
f = Fernet(key)


async def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_data = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        # Verify if the user exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user WHERE id=%s",
                           (decoded_data["id"],))
            result = cursor.fetchone()
            if not result:
                raise HHTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    details="User deleted")
        return User(id=decoded_data["id"], username=decoded_data["username"], firstname=decoded_data["firstname"],
                    lastname=decoded_data["lastname"], password=decoded_data["password"],
                    email=decoded_data["email"], rights=decoded_data["rights"], id_company=decoded_data["id_company"])
    except JWTError:
        return credentials_exception


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s",
                       (form_data.username, hashlib.sha256(
                           form_data.password.encode()).hexdigest()))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect username or password")
        data = {"id": result["id"], "username": result["username"], "firstname": result["firstname"], "lastname": result["lastname"],
                "password": result["password"], "email": result["email"], "rights": result["rights"], "id_company": result["id_company"]}
        jwt_token = jwt.encode(data, JWT_KEY, algorithm="HS256")
        return {"access_token": jwt_token, "token_type": "bearer"}


@ router.get("/current_user")
async def current_user(user: Annotated[User, Depends(decode_token)]):
    cursor.execute("SELECT name FROM company WHERE id = %s",
                   (user.id_company,))
    result = cursor.fetchone()
    return {"id": user.id, "username": user.username, "firstname": f.decrypt(user.firstname.encode()),
            "lastname": f.decrypt(user.lastname.encode()), "email": f.decrypt(user.email.encode()),
            "rights": user.rights, "company": result["name"]}
