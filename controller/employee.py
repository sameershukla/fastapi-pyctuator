from fastapi import FastAPI
from pyctuator.pyctuator import Pyctuator
from pyctuator.health.redis_health_provider import RedisHealthProvider
from pyctuator.logfile.logfile import PyctuatorLogfile

from pydantic import BaseModel
import redis
from datetime import timedelta

app = FastAPI()

pyctuator = Pyctuator(
            app,
            "FastAPI Pyctuator",
            app_url="http://localhost:8000",
            pyctuator_endpoint_url="http://localhost:8000/pyctuator",
            registration_url="http://localhost:8093/instances"
)

r = redis.Redis()
pyctuator.register_health_provider(RedisHealthProvider(r))

def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")


client = redis_connect()


class Employee(BaseModel):
    emp_id: int
    name: str
    dept: str


@app.get('/employees')
def employees():
    return {"empId": 1, "name": "Test", "dept": "IT"}

@app.get('/employees/{emp_id}')
def employees(emp_id):
    val = client.get(emp_id)
    print("Val:", val)


@app.post('/employees')
def createEmployee(employee: Employee):
    client.sadd(employee.emp_id, bytes(employee.name))
    return employee
