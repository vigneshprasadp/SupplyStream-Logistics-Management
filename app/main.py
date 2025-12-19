from fastapi import FastAPI
from app.database import engine, Base
from app.routers import supplier,product,order,shipment

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(supplier.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(shipment.router)

@app.get("/")
def read_root():
    return {"message": "Logistics Backend is running 🚚"}