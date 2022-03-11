
from asyncio import events
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from auth.models import UserModel
from auth.schemas import UserCreate
from auth.utils import get_current_user
from event.models import EventModel
from event.schemas import EventCreate, EventUpdate
from db_setup import get_db

event_router = APIRouter(prefix='/events')

@event_router.post('/create')
def create_event(
    event_schema: EventCreate,
    db: Session=Depends(get_db),
    current_user: UserCreate=Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin users can create an event'
        )

    event_model = EventModel(
        **event_schema.dict(),
        created_by=current_user.id
    )
    db.add(event_model)
    db.commit()
    db.refresh(event_model)
    return event_model


@event_router.patch('/update/{item_id}')
def update_partiall(
    item_id: int,
    event_schema: EventUpdate,
    db: Session=Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admin users can update an event'
        )

    event_model = db.query(UserModel).get(item_id)
    to_be_update = event_schema.dict(exclude_unset=True)
    event_model.__dict__.update(to_be_update)
    db.add(event_model)
    db.commit()
    db.refresh(event_model)
    return event_model
