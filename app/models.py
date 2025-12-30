from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    phone_number = Column(String(20))
    min_capacity = Column(DECIMAL(10, 2), default=50.0) # New: Minimum capacity rule

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    quantity_available = Column(Integer, nullable=False)
    volume_per_unit = Column(DECIMAL(10, 2), default=1.0) # New: Volume per unit

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    quantity_ordered = Column(Integer, nullable=False)
    total_volume = Column(DECIMAL(10, 2), default=0.0) # New: Computed volume
    shipment_id = Column(Integer, ForeignKey("shipment.shipment_id"), nullable=True) # New: Link to shipment (Many-to-One)
    status = Column(String(50), default="Pending") # New: Order status

    shipment = relationship("Shipment", back_populates="orders", foreign_keys=[shipment_id])

class Shipment(Base):
    __tablename__ = "shipment"

    shipment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=True)
    shipment_date = Column(DateTime, default=datetime.utcnow)
    estimated_arrival_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    actual_arrival_date = Column(DateTime)
    required_capacity = Column(DECIMAL(10, 2), default=0.0)
    current_load = Column(DECIMAL(10, 2), default=0.0)
    load_percentage = Column(DECIMAL(5, 2), default=0.0)
    priority = Column(String(20), default="normal")
    extra_charge = Column(DECIMAL(10, 2), default=0.0)
    total_cost = Column(DECIMAL(10, 2), default=0.0)
    cost_reason = Column(String(255), nullable=True)

    orders = relationship("Order", back_populates="shipment", foreign_keys=[Order.shipment_id])

    @property
    def order_ids(self):
        return [o.order_id for o in self.orders]