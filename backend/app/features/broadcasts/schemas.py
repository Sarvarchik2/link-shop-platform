from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .models import BroadcastStatus, BroadcastAudience

class BroadcastBase(BaseModel):
    message_text: str
    media_url: Optional[str] = None
    button_text: Optional[str] = None
    button_url: Optional[str] = None
    audience_type: BroadcastAudience = BroadcastAudience.ALL
    scheduled_at: Optional[datetime] = None

class BroadcastCreate(BroadcastBase):
    pass

class BroadcastUpdate(BaseModel):
    message_text: Optional[str] = None
    media_url: Optional[str] = None
    button_text: Optional[str] = None
    button_url: Optional[str] = None
    audience_type: Optional[BroadcastAudience] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[BroadcastStatus] = None

class BroadcastResponse(BroadcastBase):
    id: int
    shop_id: int
    status: BroadcastStatus
    sent_count: int
    failed_count: int
    total_count: int
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
