
from asyncio import events
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from auth.models import UserModel
from auth.schemas import UserCreate
from auth.utils import get_current_user
from event.models import EventModel
from event.schemas import EventCreate
from db_setup import get_db

event_router = APIRouter(prefix='/events')

@event_router.post('/create')
def create_event(
    event_schema: EventCreate,
    db: Session=Depends(get_db),
    current_user: UserCreate=Depends(get_current_user)
):
    event_model = EventModel(
        **event_schema.dict(),
        created_by=current_user.id
    )
    db.add(event_model)
    db.commit()
    db.refresh(event_model)
    return event_model
