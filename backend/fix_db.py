from app.db.session import engine
from app.db.base_class import Base

# Import all models to ensure they are registered with Base metadata
from app.features.users.models import User
from app.features.shops.models import Shop
from app.features.products.models import Product
from app.features.categories.models import Category
from app.features.brands.models import Brand
from app.features.orders.models import Order, OrderItem
from app.features.subscriptions.models import SubscriptionPlan, SubscriptionRequest
from app.features.banners.models import Banner
from app.features.offers.models import Offer
# Add other models as needed

def create_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    create_tables()
