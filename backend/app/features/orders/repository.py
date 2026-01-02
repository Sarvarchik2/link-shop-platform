from sqlalchemy.orm import Session, joinedload
from .models import Order, OrderItem
from app.features.products.models import Product
from app.features.shops.models import Shop

class OrderRepository:
    def create_order(self, db: Session, order_data: dict):
        db_order = Order(**order_data)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order

    def create_order_item(self, db: Session, item_data: dict):
        db_item = OrderItem(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def get_by_id(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()

    def get_user_orders(self, db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()

    def get_shop_orders(self, db: Session, shop_id: int):
        return db.query(Order).options(joinedload(Order.user)).filter(Order.shop_id == shop_id).order_by(Order.created_at.desc()).all()

    def get_all_orders(self, db: Session):
        return db.query(Order).options(joinedload(Order.user)).order_by(Order.created_at.desc()).all()

    def get_order_items(self, db: Session, order_id: int):
        # Join with Product and Shop to get details
        return db.query(OrderItem, Product.name, Product.image_url, Shop.slug).\
            join(Product, OrderItem.product_id == Product.id).\
            outerjoin(Shop, Product.shop_id == Shop.id).\
            filter(OrderItem.order_id == order_id).all()

    def update(self, db: Session, db_order: Order, update_data: dict):
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
        return db_order
