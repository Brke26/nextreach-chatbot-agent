from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False)
    role = Column(String(120), nullable=True)
    company = Column(String(160), nullable=False)
    website = Column(String(240), nullable=True)

    need = Column(Text, nullable=False)
    ecommerce_platform = Column(String(120), nullable=True)
    urgency = Column(String(80), nullable=False)
    budget = Column(String(80), nullable=True)
    preferred_contact = Column(String(80), nullable=True)

    lead_score = Column(Integer, default=0)
    lead_quality = Column(String(40), default="Low")
    summary = Column(Text, nullable=True)
    next_best_action = Column(Text, nullable=True)

    status = Column(String(40), default="New")
    internal_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)