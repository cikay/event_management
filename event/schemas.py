from datetime import datetime
from pydoc import describe
from datetime import datetime

from pydantic import BaseModel

class EventCreate(BaseModel):
    description: str
    total_tickets_count: int
    open_window: datetime
    start_date: datetime

