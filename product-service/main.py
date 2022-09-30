import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.post('/product')
def create_product(product: Product):
    return product.save()


@app.get('/product/{pk}')
def get_product(pk: str):
    return Product.get(pk=pk)


@app.get('/product')
def get_all_product():
    return [formatting(pk) for pk in Product.all_pks()]


@app.delete('/product/{pk}')
def delete_product(pk: str):
    return Product.delete(pk=pk)


def formatting(pk):
    product = Product.get(pk=pk)
    return {
        "pk": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }
