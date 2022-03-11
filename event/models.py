
from datetime import datetime

from sqlalchemy import (
    Column, Integer, Text, DateTime, ForeignKey, Boolean, String,
)

from db_setup import Base
from utils.sqlalchemy_utils import generate_field_value_func


class TicketModel(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)
    seat_no = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EventModel(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, index=True)
    total_tickets_count = Column(Integer, nullable=False)
    remain_tickets_count = Column(
        Integer,
        nullable=False,
        default=generate_field_value_func('total_tickets_count'),
        server_default="0"
    )
    description = Column(Text, nullable=False)
    open_window = Column(DateTime, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


    def is_within_window(self):
        remain_time = self.open_window - datetime.utcnow()
        return remain_time > 0


