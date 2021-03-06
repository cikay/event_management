from fastapi import FastAPI


from db_setup import engine
from auth.models import UserModel
from auth.controllers import auth_router 
from event.models import EventModel
from event.controllers import event_router
from ticket.controllers import ticket_router
from ticket.models import TicketModel

all_models = [
    UserModel, TicketModel, EventModel
]

for model in all_models:
    model.metadata.create_all(bind=engine)


app = FastAPI()

ALL_ROUTERS = [
    auth_router, event_router, ticket_router
]

def add_router_to_doc(routers):
    for router in routers:
        app.include_router(router)

add_router_to_doc(ALL_ROUTERS)
