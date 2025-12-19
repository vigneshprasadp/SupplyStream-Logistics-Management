from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Suppliercreate(BaseModel):
    name: str
    address: str
    contact_person: str | None = None
    phone_number: str | None = None

class Productcreate(BaseModel):
    name: str
    description: str | None = None
    unit_price: float
    quantity_available: int

class Ordercreate(BaseModel):
    product_id: int
    supplier_id: int
    order_date: datetime | None = None
    quantity_ordered: int

class Shipmentcreate(BaseModel):
    order_id: int
    shipment_date: datetime 
    estimated_arrival_date: datetime
    status: str
    actual_arrival_date: Optional[datetime] | None = None

class Supplierupdate(BaseModel):
    name: str | None = None
    address: str | None = None
    contact_person: str | None = None
    phone_number: str | None = None

class Supplierout(Suppliercreate):
    supplier_id: int
    class Config:
        orm_mode = True


class Productupdate(BaseModel):
    name: str | None = None
    description: str | None = None
    unit_price: float | None = None
    quantity_available: int | None = None

class Productout(Productcreate):
    product_id: int
    class Config:
        orm_mode = True


class Orderout(Ordercreate):
    order_id: int
    class Config:
        orm_mode = True

class Shipmentout(Shipmentcreate):
    shipment_id: int
    class Config:
        orm_mode = True

class Shipmentupdate(BaseModel):
    order_id: Optional[int] | None = None
    shipment_date: Optional[datetime] | None = None 
    estimated_arrival_date: Optional[datetime] | None = None
    status: Optional[str] | None = None
    actual_arrival_date: Optional[datetime] | None = None

