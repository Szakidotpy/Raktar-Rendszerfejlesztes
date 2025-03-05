from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from tortoise import fields, models

app = FastAPI()

# Adatbázis modellek
class Order(models.Model):
    id = fields.IntField(pk=True)
    customer_name = fields.CharField(max_length=100)
    product = fields.CharField(max_length=100)
    quantity = fields.IntField()
    status = fields.CharField(max_length=50, default="pending")
    created_at = fields.DatetimeField(auto_now_add=True)

class Order_Pydantic(BaseModel):
    customer_name: str
    product: str
    quantity: int
    status: str

# API végpontok
@app.post("/orders/")
async def create_order(order: Order_Pydantic):
    new_order = await Order.create(**order.dict())
    return {"message": "Order created", "order_id": new_order.id}

@app.get("/orders/")
async def list_orders():
    orders = await Order.all().values()
    return orders

# Adatbázis konfiguráció és migráció
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": [__name__]},
    generate_schemas=True,
    add_exception_handlers=True,
)
