# System imports
from typing import Annotated
import hashlib
import pymysql

# Libs imports
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

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


async def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_data = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        # TODO: verify that the user actually exists, for example if it was deleted since the JWT was emited
        return User(id=decoded_data["id"], name=decoded_data["name"], password=decoded_data["password"],
                    email=decoded_data["email"], rights=decoded_data["rights"], id_company=decoded_data["id_company"])
    except JWTError:
        return credentials_exception


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with connection.cursor() as cursor:
        cursor.execute(query="SELECT * FROM user WHERE email = %s AND password = %s",
                       args=(form_data.username, hashlib.sha256(form_data.password.encode()).hexdigest(),))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect username or password")
        data = {"id": result["id"], "name": form_data.username, "password": form_data.password,
                "email": result["email"], "rights": result["rights"], "id_company": result["id_company"]}
        jwt_token = jwt.encode(data, JWT_KEY, algorithm="HS256")
        return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/items/")
async def read_items(user: Annotated[User, Depends(decode_token)]):
    return "worked"
