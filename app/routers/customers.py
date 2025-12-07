# app/routers/customers.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post("/",
             response_model=schemas.CustomerRead,
             status_code=status.HTTP_201_CREATED)
def create_customer(customer_in: schemas.CustomerCreate,
                    db: Session = Depends(get_db)):
    # Проверка, что email уникален
    existing = (db.query(models.Customer)
                .filter(models.Customer.email == customer_in.email)
                .first())
    if existing:
        raise HTTPException(status_code=400,
                            detail="Email already registered")

    customer = models.Customer(**customer_in.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get("/",
            response_model=List[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    customers = (db.query(models.Customer)
                 .all())

    return customers


@router.get("/{customer_id}",
            response_model=schemas.CustomerRead)
def get_customer(customer_id: int,
                 db: Session = Depends(get_db)):
    customer = (db.query(models.Customer)
                .filter(models.Customer.id == customer_id)
                .first())

    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    return customer


@router.put("/{customer_id}",
            response_model=schemas.CustomerRead)
def update_customer(customer_id: int,
                    customer_in: schemas.CustomerUpdate,
                    db: Session = Depends(get_db)):
    customer = (db.query(models.Customer)
                .filter(models.Customer.id == customer_id)
                .first())

    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not found")

    update_data = customer_in.model_dump(exclude_unset=True)

    # Если меняем email — проверим уникальность
    new_email = update_data.get("email")
    if new_email and new_email != customer.email:
        existing = (db.query(models.Customer)
                    .filter(models.Customer.email == new_email)
                    .first())
        if existing:
            raise HTTPException(status_code=400,
                                detail="Email already registered")

    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


@router.delete("/{customer_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int,
                    db: Session = Depends(get_db)):
    customer = (db.query(models.Customer)
                .filter(models.Customer.id == customer_id)
                .first())

    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    db.delete(customer)
    db.commit()

    return None
