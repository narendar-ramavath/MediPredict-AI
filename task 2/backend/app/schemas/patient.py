from pydantic import BaseModel, EmailStr, Field, field_validator
from email_validator import validate_email
from datetime import datetime
from typing import Optional
import re
import calendar


class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=150)
    date_of_birth: str = Field(...)
    email: EmailStr = Field(...)
    glucose: float = Field(...)
    haemoglobin: float = Field(...)
    cholesterol: float = Field(...)

    @field_validator('full_name')
    @classmethod
    def trim_name(cls, v: str) -> str:
        return v.strip()

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        v = v.strip().replace('.', '/')
        parts = v.split('/')
        if len(parts) != 3:
            raise ValueError("Date must be in dd/mm/yyyy format")
        
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        
        if day < 1 or day > 31:
            raise ValueError("Invalid day")
        if month < 1 or month > 12:
            raise ValueError("Invalid month")
        if year < 1900 or year > 2100:
            raise ValueError("Invalid year")
        
        max_day = calendar.monthrange(year, month)[1]
        if day > max_day:
            raise ValueError(f"Invalid date: {calendar.month_name[month]} has only {max_day} days")
        
        input_date = datetime(year, month, day).date()
        today = datetime.now().date()
        if input_date > today:
            raise ValueError("Date of birth cannot be in the future")
        
        return f"{year:04d}-{month:02d}-{day:02d}"

    @field_validator('glucose', 'haemoglobin', 'cholesterol')
    @classmethod
    def validate_numeric(cls, v: float) -> float:
        if v != v or abs(v) == float('inf'):
            raise ValueError("Value must be a valid number")
        return v


class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=150)
    date_of_birth: Optional[str] = None
    email: Optional[EmailStr] = None
    glucose: Optional[float] = None
    haemoglobin: Optional[float] = None
    cholesterol: Optional[float] = None

    @field_validator('full_name')
    @classmethod
    def trim_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().replace('.', '/')
        parts = v.split('/')
        if len(parts) != 3:
            raise ValueError("Date must be in dd/mm/yyyy format")
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900 or year > 2100:
            raise ValueError("Invalid date")
        max_day = calendar.monthrange(year, month)[1]
        if day > max_day:
            raise ValueError(f"Invalid date: {calendar.month_name[month]} has only {max_day} days")
        input_date = datetime(year, month, day).date()
        if input_date > datetime.now().date():
            raise ValueError("Date of birth cannot be in the future")
        return f"{year:04d}-{month:02d}-{day:02d}"

    @field_validator('glucose', 'haemoglobin', 'cholesterol')
    @classmethod
    def validate_numeric(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and (v != v or abs(v) == float('inf')):
            raise ValueError("Value must be a valid number")
        return v


class PatientResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: str
    email: str
    glucose: float
    haemoglobin: float
    cholesterol: float
    remarks: Optional[str] = None
    ai_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
