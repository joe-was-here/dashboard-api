from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
import uuid


def ensure_nested_ids(data):
    """Ensure all nested objects have UUIDs"""
    if isinstance(data, dict):
        # Generate ID if not present
        if 'id' not in data or not data['id']:
            data['id'] = str(uuid.uuid4())
        # Recursively process nested objects
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                data[key] = ensure_nested_ids(value)
    elif isinstance(data, list):
        return [ensure_nested_ids(item) for item in data]
    return data


def get_patients(db: Session, cursor: str = None, limit: int = 20):
    query = db.query(models.Patient)
    
    if cursor:
        # Use cursor-based pagination for infinite scroll
        query = query.filter(models.Patient.created_at < cursor)
    
    # Order by created_at descending for newest first
    patients = query.order_by(models.Patient.created_at.desc()).limit(limit).all()
    
    # Get the cursor for the next batch (created_at of the last item)
    next_cursor = patients[-1].created_at.isoformat() if patients else None
    
    return {
        "patients": patients,
        "next_cursor": next_cursor,
        "has_more": len(patients) == limit
    }


def get_patient(db: Session, patient_id: str):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def create_patient(db: Session, patient: schemas.PatientCreate):
    # Process medical info to ensure medications have UUIDs
    medical_info = patient.medicalInfo.model_dump()
    medical_info['current_medications'] = ensure_nested_ids(medical_info.get('current_medications', []))
    
    # Process documents to ensure they have UUIDs
    documents = ensure_nested_ids([doc.model_dump() for doc in patient.documents])
    
    db_patient = models.Patient(
        first_name=patient.firstName,
        last_name=patient.lastName,
        date_of_birth=patient.dateOfBirth,
        email=patient.email,
        phone=patient.phone,
        address=patient.address.model_dump(),
        emergency_contact=patient.emergencyContact.model_dump(),
        medical_info=medical_info,
        insurance=patient.insurance.model_dump(),
        documents=documents,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: str, updates: dict):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    for key, value in updates.items():
        if key == 'medical_info' and isinstance(value, dict):
            # Ensure medications have UUIDs
            if 'current_medications' in value:
                value['current_medications'] = ensure_nested_ids(value['current_medications'])
        elif key == 'documents' and isinstance(value, list):
            # Ensure documents have UUIDs
            value = ensure_nested_ids(value)
        
        setattr(db_patient, key, value)
    
    db_patient.updated_at = date.today()
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient