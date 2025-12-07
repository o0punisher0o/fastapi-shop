# app/routers/products.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("/",
             response_model=schemas.ProductRead,
             status_code=status.HTTP_201_CREATED,)
def create_product(product_in: schemas.ProductCreate,
                   db: Session = Depends(get_db)):
    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.get("/",
            response_model=List[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    products = (db.query(models.Product)
                .all())

    return products


@router.get("/{product_id}",
            response_model=schemas.ProductRead)
def get_product(product_id: int,
                db: Session = Depends(get_db)):
    product = (db.query(models.Product)
               .filter(models.Product.id == product_id)
               .first())
    if not product:
        raise HTTPException(status_code=404,
                            detail="Product not found")

    return product


@router.put("/{product_id}",
            response_model=schemas.ProductRead)
def update_product(product_id: int,
                   product_in: schemas.ProductUpdate,
                   db: Session = Depends(get_db)):
    product = (db.query(models.Product)
               .filter(models.Product.id == product_id)
               .first())
    if not product:
        raise HTTPException(status_code=404,
                            detail="Product not found")

    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int,
                   db: Session = Depends(get_db)):
    product = (db.query(models.Product)
               .filter(models.Product.id == product_id)
               .first())
    if not product:
        raise HTTPException(status_code=404,
                            detail="Product not found")
    db.delete(product)
    db.commit()

    return None
