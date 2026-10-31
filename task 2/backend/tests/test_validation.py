import pytest
from app.schemas.patient import PatientCreate, PatientUpdate


def test_valid_patient_create():
    """Test valid patient creation data"""
    patient = PatientCreate(
        full_name="John Doe",
        date_of_birth="15/06/1990",
        email="john@example.com",
        glucose=100.5,
        haemoglobin=14.0,
        cholesterol=200.0
    )
    assert patient.full_name == "John Doe"
    assert patient.date_of_birth == "1990-06-15"


def test_invalid_email():
    """Test invalid email format"""
    with pytest.raises(ValueError, match="email"):
        PatientCreate(
            full_name="John Doe",
            date_of_birth="15/06/1990",
            email="invalid-email",
            glucose=100.5,
            haemoglobin=14.0,
            cholesterol=200.0
        )


def test_missing_domain_email():
    """Test email without proper domain"""
    with pytest.raises(ValueError):
        PatientCreate(
            full_name="John Hunter",
            date_of_birth="10/12/1990",
            email="hunter@gmail",
            glucose=94,
            haemoglobin=15,
            cholesterol=200
        )


def test_future_dob():
    """Test future date of birth"""
    with pytest.raises(ValueError, match="future"):
        PatientCreate(
            full_name="Kris Wu",
            date_of_birth="19/10/2030",
            email="kris@example.com",
            glucose=79,
            haemoglobin=16.5,
            cholesterol=197
        )


def test_impossible_date():
    """Test impossible calendar date (31 November)"""
    with pytest.raises(ValueError, match="Invalid date"):
        PatientCreate(
            full_name="Peter Larry",
            date_of_birth="31/11/2001",
            email="peter@example.com",
            glucose=88,
            haemoglobin=11.5,
            cholesterol=165
        )


def test_dotted_date_format():
    """Test dotted date format (dd.mm.yyyy)"""
    patient = PatientCreate(
        full_name="Robyn Pears",
        date_of_birth="28.01.1960",
        email="robyn@gmail.com",
        glucose=232,
        haemoglobin=13.5,
        cholesterol=180
    )
    assert patient.date_of_birth == "1960-01-28"


def test_nan_value():
    """Test NaN value rejection"""
    with pytest.raises(ValueError, match="valid number"):
        PatientCreate(
            full_name="Test",
            date_of_birth="15/06/1990",
            email="test@example.com",
            glucose=float('nan'),
            haemoglobin=14.0,
            cholesterol=200.0
        )


def test_infinity_value():
    """Test infinity value rejection"""
    with pytest.raises(ValueError, match="valid number"):
        PatientCreate(
            full_name="Test",
            date_of_birth="15/06/1990",
            email="test@example.com",
            glucose=100.5,
            haemoglobin=float('inf'),
            cholesterol=200.0
        )


def test_empty_name():
    """Test empty name after trimming"""
    with pytest.raises(ValueError):
        PatientCreate(
            full_name="   ",
            date_of_birth="15/06/1990",
            email="test@example.com",
            glucose=100.5,
            haemoglobin=14.0,
            cholesterol=200.0
        )


def test_patient_update_partial():
    """Test partial update"""
    update = PatientUpdate(email="newemail@example.com")
    assert update.email == "newemail@example.com"
    assert update.full_name is None
