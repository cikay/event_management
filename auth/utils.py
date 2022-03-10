from fastapi import HTTPException

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pytest import Session

from db_setup import get_db
from auth.controllers import oauth2_scheme, SECRET_KEY, ALGORITHM
from auth.models import UserModel

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = token_data.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    return db.query(UserModel).get(user_id)
