import os
import time

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
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


class OrderProduct(HashModel):
    product_id: str
    quantity: float

    class Meta:
        database = redis


class Order(HashModel):
    product_id: str
    fee: float
    price: float
    total: int
    quantity: int
    status: str

    class Meta:
        database = redis


@app.post('/order')
def create_order(orderproduct: OrderProduct, background_tasks: BackgroundTasks):
    req = requests.get(f"http://localhost:8001/product/{orderproduct.product_id}")
    product = req.json()
    fee = product['price'] * 0.2
    order = Order(
        product_id=orderproduct.product_id,
        fee=fee,
        quantity=orderproduct.quantity,
        price=product['price'],
        total=product['price'] + fee,
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_complete, order)
    return order


@app.get('/order/{pk}')
def get_order(pk: str):
    return Order.get(pk)


@app.get('/order')
def get_all_orders():
    return [formatting(pk) for pk in Order.all_pks()]


def formatting(pk):
    order = Order.get(pk=pk)
    return {
        "pk": order.pk,
        "product_id": order.product_id,
        "fee": order.fee,
        "total": order.total,
        "quantity": order.quantity,
        "price": order.price,
        "status": order.status
    }


def order_complete(order: Order):
    time.sleep(5)
    order.status = 'complete'
    order.save()
    redis.xadd(name='order-completed', fields=order.dict())
