from fastapi import FastAPI
from pydantic import BaseModel
from pyctuator.pyctuator import Pyctuator

app = FastAPI()

pyctuator = Pyctuator(
    app,
    "Monitoring User Service",
    app_url="http://localhost:8000",
    pyctuator_endpoint_url="http://localhost:8000/pyctuator",
    registration_url="http://localhost:8080/instances"
)


class User(BaseModel):
    id: int
    name: str
    email: str


user_details = {
    1: {
        "name": "User-1",
        "email": "user1@abc.com"
    },
    2: {
        "name": "User-2",
        "email": "user2@abc.com"
    }
}


@app.get('/users')
def users():
    return user_details


@app.get('/users/{id}')
def userById(user_id: int):
    return user_details[user_id]


@app.post('/users')
def createUser(user: User):
    id = user.id
    user_details[id] = user
    return user_details[id]
