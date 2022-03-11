from datetime import datetime
from pydoc import describe
from datetime import datetime

from pydantic import BaseModel

from utils.pydantic_utils import AllOptional

class EventCreate(BaseModel):
    description: str
    total_tickets_count: int
    open_window: datetime
    start_date: datetime
    end_date: datetime

class EventUpdate(EventCreate, metaclass=AllOptional):
    pass
