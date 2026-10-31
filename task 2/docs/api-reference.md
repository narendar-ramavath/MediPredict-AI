# MediPredict AI - API Reference

## Base URL
```
http://localhost:8000
```

## Health Check

### GET /api/health
Check API and database connectivity status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Patients

### POST /api/patients
Create a new patient record.

**Request Body:**
```json
{
  "full_name": "John Doe",
  "date_of_birth": "15/06/1990",
  "email": "john@example.com",
  "glucose": 100.5,
  "haemoglobin": 14.0,
  "cholesterol": 200.0
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-06-15",
  "email": "john@example.com",
  "glucose": 100.5,
  "haemoglobin": 14.0,
  "cholesterol": 200.0,
  "remarks": "AI-generated remark...",
  "ai_status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

**Validation Errors (422):**
```json
{
  "detail": "Date of birth cannot be in the future"
}
```

### GET /api/patients
List all patients with optional search.

**Query Parameters:**
- `search` (optional): Search by name or email

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "date_of_birth": "1990-06-15",
    "email": "john@example.com",
    "glucose": 100.5,
    "haemoglobin": 14.0,
    "cholesterol": 200.0,
    "remarks": "AI-generated remark...",
    "ai_status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": null
  }
]
```

### GET /api/patients/{patient_id}
Get a specific patient by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-06-15",
  "email": "john@example.com",
  "glucose": 100.5,
  "haemoglobin": 14.0,
  "cholesterol": 200.0,
  "remarks": "AI-generated remark...",
  "ai_status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Patient not found"
}
```

### PUT /api/patients/{patient_id}
Update a patient record.

**Request Body (all fields optional):**
```json
{
  "email": "newemail@example.com",
  "glucose": 110.0
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-06-15",
  "email": "newemail@example.com",
  "glucose": 110.0,
  "haemoglobin": 14.0,
  "cholesterol": 200.0,
  "remarks": "AI-generated remark...",
  "ai_status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

### DELETE /api/patients/{patient_id}
Delete a patient record.

**Response (200 OK):**
```json
{
  "message": "Patient deleted successfully"
}
```

### POST /api/patients/{patient_id}/analyze
Trigger AI analysis for a patient record.

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-06-15",
  "email": "john@example.com",
  "glucose": 100.5,
  "haemoglobin": 14.0,
  "cholesterol": 200.0,
  "remarks": "AI-generated remark...",
  "ai_status": "completed",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

## Validation Rules

### Full Name
- Required
- Trimmed whitespace
- Maximum 150 characters

### Date of Birth
- Required
- Format: dd/mm/yyyy or dd.mm.yyyy
- Must be a valid calendar date
- Cannot be in the future
- Stored as YYYY-MM-DD

### Email
- Required
- Must be valid email format

### Blood Values (Glucose, Haemoglobin, Cholesterol)
- Required
- Must be finite numeric values
- NaN and infinity rejected

## AI Status Values

- `pending`: AI analysis in progress
- `completed`: AI analysis successful
- `unavailable`: AI service not configured
- `failed`: AI analysis failed

## Error Responses

### 422 Unprocessable Entity
Validation error with detail message.

### 404 Not Found
Resource not found.

### 502 Bad Gateway
AI provider failure or invalid response.

### 503 Service Unavailable
AI provider unavailable.
