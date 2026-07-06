from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    role: Optional[str] = Field(default=None, max_length=120)
    company: str = Field(min_length=2, max_length=160)
    website: Optional[str] = Field(default=None, max_length=240)

    need: str = Field(min_length=10, max_length=1500)
    ecommerce_platform: Optional[str] = Field(default=None, max_length=120)
    urgency: str = Field(min_length=2, max_length=80)
    budget: Optional[str] = Field(default=None, max_length=80)
    preferred_contact: Optional[str] = Field(default=None, max_length=80)

    honeypot: Optional[str] = None


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    internal_notes: Optional[str] = None