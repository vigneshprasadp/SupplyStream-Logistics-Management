from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from datetime import datetime
from .database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    phone_number = Column(String(20))


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity_available = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    quantity_ordered = Column(Integer, nullable=False)

class Shipment(Base):
    __tablename__ = "shipment"

    shipment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    shipment_date = Column(DateTime, default=datetime.utcnow)
    estimated_arrival_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    actual_arrival_date = Column(DateTime)