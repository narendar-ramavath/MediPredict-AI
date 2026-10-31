from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.services.ai_service import AIService, AIRequest


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = PatientRepository(db)
        self.ai_service = AIService()

    async def create_patient(self, patient: PatientCreate) -> PatientResponse:
        db_patient = self.repository.create(patient)
        
        # Trigger AI analysis
        ai_request = AIRequest(
            glucose=patient.glucose,
            haemoglobin=patient.haemoglobin,
            cholesterol=patient.cholesterol
        )
        ai_response = await self.ai_service.analyze(ai_request)
        
        self.repository.update_ai_result(
            db_patient.id,
            ai_response.remarks,
            ai_response.status
        )
        
        return PatientResponse.model_validate(db_patient)

    def get_patients(self, search: Optional[str] = None) -> List[PatientResponse]:
        patients = self.repository.get_all(search)
        return [PatientResponse.model_validate(p) for p in patients]

    def get_patient(self, patient_id: int) -> Optional[PatientResponse]:
        patient = self.repository.get_by_id(patient_id)
        if patient:
            return PatientResponse.model_validate(patient)
        return None

    def update_patient(self, patient_id: int, patient_update: PatientUpdate) -> Optional[PatientResponse]:
        patient = self.repository.update(patient_id, patient_update)
        if patient:
            return PatientResponse.model_validate(patient)
        return None

    def delete_patient(self, patient_id: int) -> bool:
        return self.repository.delete(patient_id)

    async def analyze_patient(self, patient_id: int) -> Optional[PatientResponse]:
        patient = self.repository.get_by_id(patient_id)
        if not patient:
            return None
        
        ai_request = AIRequest(
            glucose=patient.glucose,
            haemoglobin=patient.haemoglobin,
            cholesterol=patient.cholesterol
        )
        ai_response = await self.ai_service.analyze(ai_request)
        
        self.repository.update_ai_result(
            patient_id,
            ai_response.remarks,
            ai_response.status
        )
        
        return PatientResponse.model_validate(patient)
