from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

@router.get("/", response_model=schemas.PatientsPaginated)
def read_patients(cursor: str = Query(None, description="Cursor for pagination"), limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return crud.get_patients(db, cursor=cursor, limit=limit)

@router.get("/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@router.put("/{patient_id}", response_model=schemas.Patient)
def update_patient_endpoint(patient_id: str, updates: dict, db: Session = Depends(get_db)):
    db_patient = crud.update_patient(db, patient_id, updates)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/{patient_id}", response_model=schemas.Patient)
def delete_patient_endpoint(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.delete_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
