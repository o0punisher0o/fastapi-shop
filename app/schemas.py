# app/schemas.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ---------- Product ----------

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[int] = None


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Customer ----------

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerRead(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Order & OrderItem ----------

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]


class OrderRead(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    status: str
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)
