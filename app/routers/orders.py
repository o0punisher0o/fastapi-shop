# app/routers/orders.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/",
             response_model=schemas.OrderRead,
             status_code=status.HTTP_201_CREATED)
def create_order(order_in: schemas.OrderCreate,
                 db: Session = Depends(get_db)):
    # Проверяем, что клиент существует
    customer = (db.query(models.Customer)
                .filter(models.Customer.id == order_in.customer_id)
                .first())
    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not found")

    if not order_in.items:
        raise HTTPException(status_code=400,
                            detail="Order must contain items")

    order = models.Order(customer_id=order_in.customer_id)
    db.add(order)
    db.flush()  # получаем order.id без коммита

    # Создаём OrderItem из списка товаров
    for item_in in order_in.items:
        product = (db.query(models.Product)
                   .filter(models.Product.id == item_in.product_id)
                   .first())
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with id {item_in.product_id} not found",
            )

        if item_in.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be positive",
            )

        # Можно добавить простейшую проверку склада
        if product.in_stock < item_in.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for product {product.id}",
            )

        # Списываем со склада
        product.in_stock -= item_in.quantity

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item_in.quantity,
            price=product.price,  # фиксируем цену на момент заказа
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)

    return order


@router.get("/",
            response_model=List[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db)):
    orders = (db.query(models.Order)
              .all())

    return orders


@router.get("/{order_id}",
            response_model=schemas.OrderRead)
def get_order(order_id: int,
              db: Session = Depends(get_db)):
    order = (db.query(models.Order)
             .filter(models.Order.id == order_id)
             .first())

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
