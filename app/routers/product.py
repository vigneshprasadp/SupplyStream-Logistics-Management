from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.models import Product
from app.database import get_db
from app.schemas import Productcreate, Productupdate, Productout

router = APIRouter(
    prefix="/products",
    tags=["products"])

@router.post("/", response_model=Productout)
def create_product(product: Productcreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        unit_price=product.unit_price,
        quantity_available=product.quantity_available,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[Productout])
def read_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/low-stock", response_model=list[Productout])
def read_low_stock_products(threshold: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.quantity_available < threshold).all()
    return products

@router.get("/{product_id}", response_model=Productout)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Productout)
def update_product(product_id: int, product: Productupdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for var, value in vars(product).items():
        if value is not None:
            setattr(db_product, var, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}/adjust-stock", response_model=Productout)
def adjust_product_stock(product_id: int, amount: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.quantity_available += amount
    if db_product.quantity_available < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
        
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int,db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404,detail="product not found")
    db.delete(db_product)
    db.commit()
    return {"detail":"deleted product successful"}
