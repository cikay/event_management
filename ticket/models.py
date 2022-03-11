
from datetime import datetime

from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey, Boolean, String,
)

from db_setup import Base


class TicketModel(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)
    seat_no = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
