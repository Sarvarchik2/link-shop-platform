from app.db.session import SessionLocal
from app.features.banners.service import BannerService
from app.features.banners.router import BannerSchema

def test_banner_service():
    db = SessionLocal()
    service = BannerService()
    try:
        print("Testing get_banners for 'premium-eyewear'...")
        banners = service.get_banners(db, shop_slug="premium-eyewear")
        print(f"Banners found: {len(banners)}")
        for b in banners:
            print(f"Banner ID: {b.id}, Title: {b.title}")
            print(f"  badge_text: {b.badge_text} ({type(b.badge_text)})")
            print(f"  subtitle: {b.subtitle} ({type(b.subtitle)})")
            print(f"  button_text: {b.button_text} ({type(b.button_text)})")
            print(f"  button_link: {b.button_link} ({type(b.button_link)})")
            print(f"  image_url: {b.image_url} ({type(b.image_url)})")
            
            try:
                # SQLAlchemy model to Pydantic
                schema = BannerSchema.model_validate(b)
                print("  ✅ Schema Validation Passed")
            except Exception as ve:
                print(f"  ❌ Schema Validation Failed: {ve}")

    except Exception as e:
        print(f"CAUGHT ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_banner_service()
