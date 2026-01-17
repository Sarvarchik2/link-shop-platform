from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text
import enum
from datetime import datetime
from app.db.base_class import Base

class BroadcastStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    SENDING = "sending"
    COMPLETED = "completed"
    FAILED = "failed"

class BroadcastAudience(str, enum.Enum):
    ALL = "all"
    RECENT = "recent"

class Broadcast(Base):
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=False, index=True)
    message_text = Column(Text, nullable=False)
    media_url = Column(String, nullable=True)
    button_text = Column(String, nullable=True)
    button_url = Column(String, nullable=True)
    audience_type = Column(SQLEnum(BroadcastAudience), default=BroadcastAudience.ALL)
    status = Column(SQLEnum(BroadcastStatus), default=BroadcastStatus.DRAFT)
    sent_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
