from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, patient: PatientCreate) -> Patient:
        db_patient = Patient(
            full_name=patient.full_name,
            date_of_birth=patient.date_of_birth,
            email=patient.email,
            glucose=patient.glucose,
            haemoglobin=patient.haemoglobin,
            cholesterol=patient.cholesterol,
            ai_status="pending"
        )
        self.db.add(db_patient)
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def get_all(self, search: Optional[str] = None) -> List[Patient]:
        query = self.db.query(Patient)
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                (Patient.full_name.ilike(search_pattern)) |
                (Patient.email.ilike(search_pattern))
            )
        return query.order_by(Patient.created_at.desc()).all()

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        return self.db.query(Patient).filter(Patient.id == patient_id).first()

    def update(self, patient_id: int, patient_update: PatientUpdate) -> Optional[Patient]:
        db_patient = self.get_by_id(patient_id)
        if not db_patient:
            return None
        
        update_data = patient_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_patient, field, value)
        
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient

    def delete(self, patient_id: int) -> bool:
        db_patient = self.get_by_id(patient_id)
        if not db_patient:
            return False
        
        self.db.delete(db_patient)
        self.db.commit()
        return True

    def update_ai_result(self, patient_id: int, remarks: str, ai_status: str) -> Optional[Patient]:
        db_patient = self.get_by_id(patient_id)
        if not db_patient:
            return None
        
        db_patient.remarks = remarks
        db_patient.ai_status = ai_status
        self.db.commit()
        self.db.refresh(db_patient)
        return db_patient
