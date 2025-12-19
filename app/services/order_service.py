from app.models import Product
from app.models import Order
from sqlalchemy.orm import Session


def check_stock_availabilty(product_id: int, quantity: int, db: Session ) -> bool:
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product and product.quantity_available >= quantity:
        return True
    return False