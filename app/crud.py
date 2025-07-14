from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
import uuid


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
    db_patient = models.Patient(
        id=str(uuid.uuid4()),
        first_name=patient.firstName,
        last_name=patient.lastName,
        date_of_birth=patient.dateOfBirth,
        email=patient.email,
        phone=patient.phone,
        address=patient.address.dict(),
        emergency_contact=patient.emergencyContact.dict(),
        medical_info=patient.medicalInfo.dict(),
        insurance=patient.insurance.dict(),
        documents=[doc.model_dump() for doc in patient.documents],
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