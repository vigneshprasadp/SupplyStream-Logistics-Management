from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models import Supplier, Order, Shipment
from app.database import get_db
from app.schemas import Suppliercreate, Supplierupdate, Supplierout, Orderout, Shipmentout

router = APIRouter(
    prefix="/suppliers",
    tags=["suppliers"],
)

@router.post("/", response_model=Supplierout)
def create_supplier(supplier: Suppliercreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(
        name=supplier.name,
        address=supplier.address,
        contact_person=supplier.contact_person,
        phone_number=supplier.phone_number,
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.get("/", response_model=list[Supplierout])
def read_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return suppliers

@router.get("/{supplier_id}", response_model=Supplierout)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@router.put("/{supplier_id}", response_model=Supplierout)
def update_supplier(supplier_id: int, supplier: Supplierupdate, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    for var,value in vars(supplier).items():
        if value is not None:
            setattr(db_supplier, var, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(db_supplier)
    db.commit()
    return {"detail": "Supplier deleted successfully"}

@router.get("/{supplier_id}/orders", response_model=list[Orderout])
def read_supplier_orders(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    orders = db.query(Order).filter(Order.supplier_id == supplier_id).all()
    return orders

@router.get("/{supplier_id}/shipments", response_model=list[Shipmentout])
def read_supplier_shipments(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    # Shipments are linked to Orders, which are linked to Suppliers
    shipments = db.query(Shipment).join(Order).filter(Order.supplier_id == supplier_id).all()
    return shipments
