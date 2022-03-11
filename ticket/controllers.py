
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from auth.utils import get_db, get_current_user 
from auth.models import UserModel
from event.models import EventModel
from ticket.schemas import TicketCreate
from ticket.models import TicketModel

ticket_router = APIRouter(prefix='/tickets')

@ticket_router.post('/create')
def create_ticket(
    ticket_schema: TicketCreate,
    db: Session=Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    event_model = db.query(EventModel).get(ticket_schema.event_id)
    if event_model.remain_tickets_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No tickets available'
        )

    ticket_model = TicketModel(
        **ticket_schema.dict(),
        user_id=current_user.id,
        is_booked=True
    )
    db.add(ticket_model)
    db.commit()
    db.refresh(ticket_model)
    return ticket_model


@ticket_router.get('/')
def list_tickets(
    db: Session=Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    return db.query(TicketModel).filter(
        TicketModel.user_id == current_user.id
    ).all()


@ticket_router.get('/{item_id}')
def retrieve_ticket(
    item_id: int,
    db: Session=Depends(get_db),
    current_user: UserModel=Depends(get_current_user)
):
    return db.query(TicketModel).get(item_id)
