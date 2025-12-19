from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order, Product, Shipment
from app.database import get_db
from app.schemas import Ordercreate, Orderout
from app.services.order_service import check_stock_availabilty
from datetime import datetime

router = APIRouter(
    prefix="/orders",
    tags=["orders"],)

@router.post("/", response_model=Orderout)
def create_order(order: Ordercreate, db: Session = Depends(get_db)):
    if not check_stock_availabilty(order.product_id, order.quantity_ordered, db):
        raise HTTPException(status_code=400, detail="Insufficient stock available")
    
    # Reduce stock
    product = db.query(Product).filter(Product.product_id == order.product_id).first()
    product.quantity_available -= order.quantity_ordered
    
    db_order = Order(
        product_id=order.product_id,
        supplier_id=order.supplier_id,
        order_date=order.order_date or datetime.utcnow(),
        quantity_ordered=order.quantity_ordered,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=list[Orderout])
def read_orders(db: Session = Depends(get_db)):
    order = db.query(Order).all()
    return order

@router.get("/date-range", response_model=list[Orderout])
def read_orders_by_date_range(start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.order_date >= start_date, Order.order_date <= end_date).all()
    return orders

@router.get("/product/{product_id}", response_model=list[Orderout])
def read_orders_by_product(product_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.product_id == product_id).all()
    return orders

@router.get("/supplier/{supplier_id}", response_model=list[Orderout])
def read_orders_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.supplier_id == supplier_id).all()
    return orders

@router.get("/{order_id}", response_model=Orderout)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if order is delivered
    shipment = db.query(Shipment).filter(Shipment.order_id == order_id).first()
    if shipment and shipment.status == "Delivered":
        raise HTTPException(status_code=400, detail="Cannot cancel order that has been delivered")
    
    # Restore stock
    product = db.query(Product).filter(Product.product_id == db_order.product_id).first()
    if product:
        product.quantity_available += db_order.quantity_ordered
    
    db.delete(db_order)
    db.commit()
    return {"detail": "Order cancelled and stock restored successfully"}