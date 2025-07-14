# app/models.py
from sqlalchemy import Column, String, Date, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    date_of_birth = Column(Date)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(JSON)
    emergency_contact = Column(JSON)
    medical_info = Column(JSON)
    insurance = Column(JSON)
    documents = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default='now()')
    updated_at = Column(DateTime(timezone=True), server_default='now()', onupdate='now()')