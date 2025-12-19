from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Shipment
from app.database import get_db
from app.schemas import Shipmentcreate, Shipmentout, Shipmentupdate
from datetime import datetime

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)

@router.post("/", response_model=Shipmentout)
def create_shipment(shipment: Shipmentcreate, db: Session = Depends(get_db)):
    db_shipment = Shipment(
        order_id=shipment.order_id,
        shipment_date=shipment.shipment_date,
        estimated_arrival_date=shipment.estimated_arrival_date,
        status=shipment.status,
        actual_arrival_date=shipment.actual_arrival_date,
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@router.get("/", response_model=list[Shipmentout])
def read_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments

@router.get("/delayed", response_model=list[Shipmentout])
def read_delayed_shipments(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    # Delayed if actual arrival > estimated OR (not arrived yet and now > estimated)
    # SQLAlchemy filter for OR condition
    from sqlalchemy import or_
    shipments = db.query(Shipment).filter(
        or_(
            Shipment.actual_arrival_date > Shipment.estimated_arrival_date,
            (Shipment.actual_arrival_date == None) & (now > Shipment.estimated_arrival_date)
        )
    ).all()
    return shipments

@router.get("/on-time", response_model=list[Shipmentout])
def read_ontime_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).filter(
        Shipment.actual_arrival_date <= Shipment.estimated_arrival_date
    ).all()
    return shipments

@router.get("/order/{order_id}", response_model=list[Shipmentout])
def read_shipments_by_order(order_id: int, db: Session = Depends(get_db)):
    shipments = db.query(Shipment).filter(Shipment.order_id == order_id).all()
    return shipments

@router.get("/{shipment_id}", response_model=Shipmentout)
def read_shipment(shipment_id: int, db: Session = Depends(get_db)):
    db_shipment = db.query(Shipment).filter(Shipment.shipment_id == shipment_id).first()
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@router.put("/{shipment_id}", response_model=Shipmentout)
def update_shipment(shipment_id: int, shipment: Shipmentupdate, db: Session = Depends(get_db)):
    db_shipment = db.query(Shipment).filter(Shipment.shipment_id == shipment_id).first()
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    for key, value in shipment.dict(exclude_unset=True).items():
        setattr(db_shipment, key, value)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@router.put("/{shipment_id}/arrival", response_model=Shipmentout)
def update_arrival_date(shipment_id: int, actual_arrival_date: datetime, db: Session = Depends(get_db)):
    db_shipment = db.query(Shipment).filter(Shipment.shipment_id == shipment_id).first()
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    db_shipment.actual_arrival_date = actual_arrival_date
    db.commit()
    db.refresh(db_shipment)
    return db_shipment