from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Shipment, Order, Supplier
from app.database import get_db
from app.schemas import Shipmentcreate, Shipmentout, Shipmentupdate
from datetime import datetime

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)

@router.post("/", response_model=Shipmentout)
def create_shipment(shipment: Shipmentcreate, db: Session = Depends(get_db)):
    # 1. Gather Orders
    target_orders = []
    if shipment.order_ids:
        target_orders = db.query(Order).filter(Order.order_id.in_(shipment.order_ids)).all()
    elif shipment.order_id:
        o = db.query(Order).filter(Order.order_id == shipment.order_id).first()
        if o: target_orders = [o]
    
    if not target_orders:
        raise HTTPException(status_code=400, detail="No valid orders specified")

    # 2. Validation (Same Supplier)
    supplier_id = target_orders[0].supplier_id
    if any(o.supplier_id != supplier_id for o in target_orders):
        raise HTTPException(status_code=400, detail="All orders must be from the same supplier")

    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    min_cap = float(supplier.min_capacity) if supplier.min_capacity else 0.0

    # 3. Calculate Load
    current_load = sum(float(o.total_volume or 0) for o in target_orders)
    
    # 4. Status & Logic
    final_status = shipment.status
    extra_charge = 0.0
    cost_reason = None
    
    # Priority Logic
    if shipment.priority == "urgent":
        if current_load < min_cap:
             # Urgent Penalty
             shortfall = min_cap - current_load
             extra_charge = shortfall * 10 # Example: $10 per missing volume unit
             cost_reason = "Urgent dispatch below capacity"
    else:
        # Normal
        if current_load < min_cap:
             final_status = "Waiting" # Override status to Waiting
        else:
             if final_status == "Pending": final_status = "Planning"

    # 5. Create Shipment
    db_shipment = Shipment(
        order_id=target_orders[0].order_id, # Link primary order for legacy ref
        shipment_date=shipment.shipment_date,
        estimated_arrival_date=shipment.estimated_arrival_date,
        status=final_status,
        required_capacity=min_cap,
        current_load=current_load,
        load_percentage=(current_load/min_cap*100) if min_cap > 0 else 100,
        priority=shipment.priority,
        extra_charge=extra_charge,
        total_cost=extra_charge, # Set total cost
        cost_reason=cost_reason,
        actual_arrival_date=shipment.actual_arrival_date
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)

    # 6. Update Orders
    for o in target_orders:
        o.shipment_id = db_shipment.shipment_id
        o.status = "Scheduled" if final_status != "Waiting" else "Waiting"
        db.add(o)
    db.commit()

    return db_shipment

@router.get("/", response_model=list[Shipmentout])
def read_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return shipments

@router.get("/delayed", response_model=list[Shipmentout])
def read_delayed_shipments(db: Session = Depends(get_db)):
    now = datetime.utcnow()
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