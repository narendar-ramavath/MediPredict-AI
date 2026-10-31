import pytest
from fastapi import status


def test_create_patient(client):
    """Test creating a patient"""
    response = client.post("/api/patients", json={
        "full_name": "Test Patient",
        "date_of_birth": "15/06/1990",
        "email": "test@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["full_name"] == "Test Patient"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_get_patients(client):
    """Test getting all patients"""
    # Create a patient first
    client.post("/api/patients", json={
        "full_name": "Test Patient",
        "date_of_birth": "15/06/1990",
        "email": "test@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    
    response = client.get("/api/patients")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_patient_by_id(client):
    """Test getting a specific patient"""
    # Create a patient first
    create_response = client.post("/api/patients", json={
        "full_name": "Test Patient",
        "date_of_birth": "15/06/1990",
        "email": "test@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    patient_id = create_response.json()["id"]
    
    response = client.get(f"/api/patients/{patient_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == patient_id
    assert data["full_name"] == "Test Patient"


def test_get_nonexistent_patient(client):
    """Test getting a non-existent patient"""
    response = client.get("/api/patients/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_patient(client):
    """Test updating a patient"""
    # Create a patient first
    create_response = client.post("/api/patients", json={
        "full_name": "Test Patient",
        "date_of_birth": "15/06/1990",
        "email": "test@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    patient_id = create_response.json()["id"]
    
    # Update the patient
    response = client.put(f"/api/patients/{patient_id}", json={
        "email": "updated@example.com"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "updated@example.com"


def test_delete_patient(client):
    """Test deleting a patient"""
    # Create a patient first
    create_response = client.post("/api/patients", json={
        "full_name": "Test Patient",
        "date_of_birth": "15/06/1990",
        "email": "test@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    patient_id = create_response.json()["id"]
    
    # Delete the patient
    response = client.delete(f"/api/patients/{patient_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify deletion
    get_response = client.get(f"/api/patients/{patient_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_duplicate_patients_allowed(client):
    """Test that duplicate patients (same name and email) are allowed"""
    patient_data = {
        "full_name": "Robyn Pears",
        "date_of_birth": "28/01/1960",
        "email": "robyn@gmail.com",
        "glucose": 232,
        "haemoglobin": 13.5,
        "cholesterol": 180
    }
    
    # Create first patient
    response1 = client.post("/api/patients", json=patient_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Create duplicate patient
    response2 = client.post("/api/patients", json=patient_data)
    assert response2.status_code == status.HTTP_201_CREATED
    
    # Verify both exist
    list_response = client.get("/api/patients")
    patients = list_response.json()
    robyn_patients = [p for p in patients if p["full_name"] == "Robyn Pears"]
    assert len(robyn_patients) == 2


def test_search_patients(client):
    """Test searching patients"""
    # Create patients
    client.post("/api/patients", json={
        "full_name": "John Doe",
        "date_of_birth": "15/06/1990",
        "email": "john@example.com",
        "glucose": 100.5,
        "haemoglobin": 14.0,
        "cholesterol": 200.0
    })
    client.post("/api/patients", json={
        "full_name": "Jane Smith",
        "date_of_birth": "20/05/1985",
        "email": "jane@example.com",
        "glucose": 95.0,
        "haemoglobin": 13.5,
        "cholesterol": 190.0
    })
    
    # Search by name
    response = client.get("/api/patients?search=John")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["full_name"] == "John Doe"
