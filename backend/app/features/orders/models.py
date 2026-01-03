from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
from app.features.users.models import User

class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=True)
    status = Column(String, default="pending")
    total_price = Column(Float, nullable=False)
    delivery_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    delivery_address = Column(String, nullable=True)
    delivery_city = Column(String, nullable=True)
    delivery_phone = Column(String, nullable=True)
    recipient_name = Column(String, nullable=True)
    payment_method = Column(String, default="cash")
    notes = Column(String, nullable=True)
    
    user = relationship("User")

class OrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    selected_color = Column(String, nullable=True)
    selected_size = Column(String, nullable=True)
