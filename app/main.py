# app/main.py
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import products, customers, orders
from app import models


# Создаём таблицы (для простоты — при старте приложения)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FastAPI Shop",
    version="1.0.0",
)


# Подключаем роутеры
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI Shop is running"}

