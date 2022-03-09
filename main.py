from fastapi import FastAPI


from db_setup import engine
from auth.models import UserModel
from event.models import TicketModel, EventModel


all_models = [
    UserModel, TicketModel, EventModel
]

for model in all_models:
    model.metadata.create_all(bind=engine)


app = FastAPI()
