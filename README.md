# FastAPI Shop

Простое приложение интернет-магазина, реализованное на FastAPI.
Поддерживает сущности:

- Products (товары)
- Customers (клиенты)
- Orders (заказы)

База данных — SQLite.
API-документация доступна по адресу:
http://127.0.0.1:8000/docs

Стек технологий
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Docker

---

Локальный запуск (без Docker)
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу:
```bash
http://127.0.0.1:8000
```


Запуск через Docker
Сборка образа:
```bash
docker build -t fastapi-shop .
```

Запуск контейнера:
```bash
docker run -p 8000:8000 fastapi-shop
```

---

Тестовые данные и примеры запросов
Ниже приведены готовые JSON-объекты для проверки API в Swagger или Postman.

1. Создание товара

POST /products
```bash
{
  "name": "Laptop Lenovo ThinkPad",
  "description": "14 inch, Intel i7, 16GB RAM",
  "price": 1099.99,
  "in_stock": 20
}
```

2. Обновление товара

PUT /products/1
```bash
{
  "price": 999.99,
  "in_stock": 15
}
```

3. Создание клиента

POST /customers
```bash
{
  "name": "Ivan Ivanov",
  "email": "ivan@example.com",
  "phone": "+7 700 123 45 67"
}
```

4. Создание заказа

POST /orders
```bash
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

---

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc