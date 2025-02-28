from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests
import time
from fastapi.background import BackgroundTasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Correct Redis connection
redis = get_redis_connection(
    host="localhost",  # Use "redis" if running in Docker
    port=6379,  # Redis default port
    password="123456",  # Ensure this is a string
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refund

    class Meta:
        database = redis

@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)

@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    # Ensure correct service URL
    req = requests.get(f'http://localhost:8000/products/{body["id"]}')
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    
    # Exclude 'pk' to avoid serialization issues
    redis.xadd('order_completed', order.dict(exclude={'pk'}), '*')

from fastapi import FastAPI



@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}
