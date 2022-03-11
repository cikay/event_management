from pydantic import BaseModel


class TicketCreate(BaseModel):
    event_id: int
    seat_no: str
