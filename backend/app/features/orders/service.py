from sqlalchemy.orm import Session
from fastapi import HTTPException
from .repository import OrderRepository
from .schemas import OrderCreate
from app.features.products.service import ProductService
from app.features.shops.service import ShopService

class OrderService:
    def __init__(self):
        self.repository = OrderRepository()
        self.product_service = ProductService()
        self.shop_service = ShopService()

    def create_order(self, db: Session, order_in: OrderCreate, user_id: int, shop_slug: str = None):
        total_price = 0.0
        shop_id = None
        
        if shop_slug:
            shop = self.shop_service.get_shop_by_slug(db, shop_slug, check_active=True)
            shop_id = shop.id
            
        # 1. Calc total price and validate products
        order_items_to_create = []
        for item in order_in.items:
            product = self.product_service.get_product(db, item.product_id)
            item_price = product.price * (1 - product.discount / 100)
            total_price += item_price * item.quantity
            
            order_items_to_create.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item_price,
                "selected_color": item.selected_color,
                "selected_size": item.selected_size
            })
            
        # 2. Calculate Delivery Cost
        delivery_cost = 0.0
        if shop_id:
            shop = self.shop_service.get_shop_by_id(db, shop_id)
            settings = shop.delivery_settings or {}
            delivery_type = settings.get("type", "free")
            
            if delivery_type == "fixed":
                delivery_cost = float(settings.get("price", 0))
            elif delivery_type == "regional":
                regions = settings.get("regions", {})
                city = order_in.delivery_city
                # Try exact match or fallback to 'Boshqa'
                delivery_cost = float(regions.get(city, regions.get("Boshqa", 0)))

        # Add delivery to total
        total_price += delivery_cost

        # 3. Create order record
        order_data = order_in.model_dump(exclude={"items"})
        order_data.update({
            "user_id": user_id,
            "shop_id": shop_id,
            "total_price": total_price,
            "delivery_cost": delivery_cost,
            "status": "pending"
        })
        db_order = self.repository.create_order(db, order_data)
        
        # 4. Create items
        for item_data in order_items_to_create:
            item_data["order_id"] = db_order.id
            self.repository.create_order_item(db, item_data)
            
        return db_order

    def get_order_details(self, db: Session, order_id: int, current_user):
        order = self.repository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
        # Auth check
        if current_user.role != "platform_admin" and order.user_id != current_user.id:
            # Maybe check if they are shop owner too
            shop = self.shop_service.get_shop_by_id(db, order.shop_id) if order.shop_id else None
            if not shop or shop.owner_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
                
        items_with_details = self.repository.get_order_items(db, order_id)
        
        items_list = []
        for item, p_name, p_image, s_slug in items_with_details:
            items_list.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "product_name": p_name,
                "product_image": p_image,
                "selected_color": item.selected_color,
                "selected_size": item.selected_size,
                "shop_slug": s_slug
            })
            
        result = order.__dict__.copy()
        result.pop("_sa_instance_state", None)
        result["items"] = items_list
        return result

    def _populate_order_items(self, db: Session, orders):
        result = []
        for order in orders:
            items_with_details = self.repository.get_order_items(db, order.id)
            items_list = []
            for item, p_name, p_image, s_slug in items_with_details:
                items_list.append({
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                    "product_name": p_name,
                    "product_image": p_image,
                    "selected_color": item.selected_color,
                    "selected_size": item.selected_size,
                    "shop_slug": s_slug
                })
            
            order_dict = order.__dict__.copy()
            order_dict.pop("_sa_instance_state", None)
            order_dict["items"] = items_list
            order_dict["user"] = order.user  # Attach user for schema validation
            result.append(order_dict)
        return result

    def get_user_orders(self, db: Session, user_id: int):
        orders = self.repository.get_user_orders(db, user_id)
        return self._populate_order_items(db, orders)

    def get_shop_orders(self, db: Session, shop_slug: str, current_user):
        shop = self.shop_service.get_shop_by_slug(db, shop_slug)
        if current_user.role != "platform_admin" and shop.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        orders = self.repository.get_shop_orders(db, shop.id)
        return self._populate_order_items(db, orders)

    def get_all_orders_for_admin(self, db: Session):
        orders = self.repository.get_all_orders(db)
        return self._populate_order_items(db, orders)

    def update_order_status(self, db: Session, order_id: int, new_status: str, current_user):
        order = self.repository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
        # Check permissions (only shop owner or platform admin)
        shop = self.shop_service.get_shop_by_id(db, order.shop_id) if order.shop_id else None
        if current_user.role != "platform_admin" and (not shop or shop.owner_id != current_user.id):
            raise HTTPException(status_code=403, detail="Not authorized")
            
        old_status = order.status
        updated_order = self.repository.update(db, order, {"status": new_status})
        
        # If status changed to delivered, update stock
        if new_status == "delivered" and old_status != "delivered":
            items = self.repository.get_order_items(db, order_id)
            for item, _, _, _ in items:
                product = self.product_service.get_product(db, item.product_id)
                new_stock = max(0, product.stock - item.quantity)
                self.product_service.repository.update(db, product, {"stock": new_stock})
                
        return updated_order
