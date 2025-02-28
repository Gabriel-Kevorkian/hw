from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']

)


redis = get_redis_connection(
    host="localhost",  # Use "redis" if running in Docker
    port=6379,  # Redis default port
    password="123456",  # Ensure this is a string
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return{
        'id':product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI backend!"}
