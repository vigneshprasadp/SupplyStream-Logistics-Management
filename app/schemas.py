from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Suppliercreate(BaseModel):
    name: str
    address: str
    contact_person: str | None = None
    phone_number: str | None = None
    min_capacity: float | None = 50.0

class Productcreate(BaseModel):
    name: str
    description: str | None = None
    unit_price: float
    quantity_available: int
    volume_per_unit: float | None = 1.0

class Ordercreate(BaseModel):
    product_id: int
    supplier_id: int
    order_date: datetime | None = None
    quantity_ordered: int

class Shipmentcreate(BaseModel):
    order_id: int | None = None # Made optional
    order_ids: list[int] | None = None # New: For consolidation
    shipment_date: datetime 
    estimated_arrival_date: datetime
    status: str
    priority: str = "normal" # normal / urgent
    actual_arrival_date: Optional[datetime] | None = None

class Supplierupdate(BaseModel):
    name: str | None = None
    address: str | None = None
    contact_person: str | None = None
    phone_number: str | None = None
    min_capacity: float | None = None

class Supplierout(Suppliercreate):
    supplier_id: int
    class Config:
        orm_mode = True


class Productupdate(BaseModel):
    name: str | None = None
    description: str | None = None
    unit_price: float | None = None
    quantity_available: int | None = None
    volume_per_unit: float | None = None

class Productout(Productcreate):
    product_id: int
    class Config:
        orm_mode = True


class Orderout(Ordercreate):
    order_id: int
    total_volume: float | None = 0.0
    status: str | None = None
    shipment_id: int | None = None
    class Config:
        orm_mode = True

class Shipmentout(Shipmentcreate):
    shipment_id: int
    required_capacity: float | None = 0.0
    current_load: float | None = 0.0
    load_percentage: float | None = 0.0
    extra_charge: float | None = 0.0
    total_cost: float | None = 0.0
    cost_reason: str | None = None
    
    class Config:
        orm_mode = True

class Shipmentupdate(BaseModel):
    order_id: Optional[int] | None = None
    shipment_date: Optional[datetime] | None = None 
    estimated_arrival_date: Optional[datetime] | None = None
    status: Optional[str] | None = None
    actual_arrival_date: Optional[datetime] | None = None
    priority: Optional[str] | None = None

