# MediPredict AI

Patient record management with AI-generated informational remarks.

## Features
- CRUD operations for patient records
- Blood test value tracking (glucose, haemoglobin, cholesterol)
- AI integration for informational remarks
- Strict validation (dates, emails, numeric values)
- Search functionality
- Responsive UI

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite, Pydantic
- **Frontend**: React, Vite, Tailwind CSS, React Router

## Installation

### Backend
```bash
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables
Edit `backend/.env`:
```env
AI_API_KEY=your_key_here
```

## API Endpoints
- `GET /api/health` - Health check
- `POST /api/patients` - Create patient
- `GET /api/patients` - List patients
- `GET /api/patients/{id}` - Get patient
- `PUT /api/patients/{id}` - Update patient
- `DELETE /api/patients/{id}` - Delete patient
- `POST /api/patients/{id}/analyze` - AI analysis

## Testing
```bash
cd backend
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -q
```

## Important
AI-generated information is for demonstration only, not medical diagnosis.
