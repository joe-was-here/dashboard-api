# app/schemas.py
import uuid
from pydantic import BaseModel, EmailStr, ConfigDict # Import ConfigDict
from typing import List, Optional, Literal
from datetime import date, datetime # Import datetime

def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(p.title() for p in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

class Address(CamelModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str

class EmergencyContact(CamelModel):
    name: str
    relationship: str
    phone: str
    email: Optional[EmailStr] = None

class Medication(CamelModel):
    id: str
    name: str
    dosage: str
    frequency: str
    prescribed_by: str
    start_date: date
    end_date: Optional[date] = None
    is_active: bool

class InsuranceInfo(CamelModel):
    provider: str
    policy_number: str
    group_number: Optional[str] = None
    effective_date: date
    expiration_date: Optional[date] = None
    copay: float
    deductible: float

class Document(CamelModel):
    id: str
    type: Literal[
        'medical_record', 'insurance_card', 'photo_id', 'test_result', 'other'
    ]
    name: str
    upload_date: date
    file_size: int
    mime_type: str
    url: str

class MedicalInfo(CamelModel):
    allergies: List[str]
    current_medications: List[Medication]
    conditions: List[str]
    blood_type: Literal['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    last_visit: date
    status: Literal['active', 'inactive', 'critical']

class PatientBase(CamelModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    address: 'Address'
    emergency_contact: 'EmergencyContact'
    medical_info: 'MedicalInfo'
    insurance: 'InsuranceInfo'
    documents: List['Document']

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class PatientsPaginated(CamelModel):
    patients: List[Patient]
    next_cursor: Optional[str] = None
    has_more: bool