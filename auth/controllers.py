
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext



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
        password=hashed_password
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {
        'username': user_model.username,
        'firstname': user_model.firstname,
        'lastname': user_model.lastname,
        'id': user_model.id
    }


def generate_hash_password(plain_password):
    return pwd_context.hash(plain_password)
