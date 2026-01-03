from pydantic import BaseModel
from typing import Optional

class ShopBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

class ShopCreate(ShopBase):
    pass

try:
    # Test with empty string for optional fields (what frontend sends)
    s = ShopCreate(name="test", slug="test-slug", description="", logo_url="")
    print("Empty strings are VALID")
    print(s.model_dump())
except Exception as e:
    print("Empty strings are INVALID")
    print(e)
