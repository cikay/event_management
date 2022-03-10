from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt


from auth.schemas import UserCreate
from auth.models import UserModel
from db_setup import get_db

auth_router = APIRouter(prefix='/users')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post("/create")
async def create(user_schema: UserCreate, db: Session = Depends(get_db)):
    hashed_password = generate_hash_password(user_schema.password)
    user_model = UserModel(
        firstname=user_schema.firstname,
        lastname=user_schema.lastname,
        username=user_schema.username,
        is_admin=user_schema.is_admin,
        password=hashed_password
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {
        'username': user_model.username,
        'firstname': user_model.firstname,
        'lastname': user_model.lastname,
        'id': user_model.id,
        'is_admin': user_model.is_admin
    }


@auth_router.post("/login")
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session=Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()

    if not is_authenticated(credentials.password, user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


def generate_hash_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def is_authenticated(plain_password, user):
    return user and verify_password(plain_password, user.password)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
