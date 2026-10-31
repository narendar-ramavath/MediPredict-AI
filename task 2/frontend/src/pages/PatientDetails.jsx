import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Edit, Trash2, RefreshCw } from 'lucide-react';
import StatusBadge from '../components/StatusBadge';
import { patientApi } from '../services/patientApi';

const PatientDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [retrying, setRetrying] = useState(false);

  useEffect(() => {
    loadPatient();
  }, [id]);

  const loadPatient = async () => {
    try {
      setLoading(true);
      const response = await patientApi.getById(id);
      setPatient(response.data);
    } catch (error) {
      console.error('Failed to load patient:', error);
      navigate('/patients');
    } finally {
      setLoading(false);
    }
  };

  const handleRetryAI = async () => {
    try {
      setRetrying(true);
      await patientApi.analyze(id);
      loadPatient();
    } catch (error) {
      console.error('Failed to retry AI analysis:', error);
    } finally {
      setRetrying(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this patient record?')) {
      try {
        await patientApi.delete(id);
        navigate('/patients');
      } catch (error) {
        console.error('Failed to delete patient:', error);
        alert('Failed to delete patient record');
      }
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading patient details...</div>;
  }

  if (!patient) {
    return <div className="p-8 text-center text-gray-500">Patient not found</div>;
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <button
          onClick={() => navigate('/patients')}
          className="flex items-center gap-2 text-navy-600 hover:text-navy-800 mb-4"
        >
          <ArrowLeft size={20} />
          Back to Patients
        </button>
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-3xl font-bold text-navy-900">{patient.full_name}</h2>
            <p className="text-gray-600 mt-2">Patient record details</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => navigate(`/patients/${patient.id}/edit`)}
              className="flex items-center gap-2 px-4 py-2 bg-navy-600 text-white rounded-lg hover:bg-navy-700 transition-colors"
            >
              <Edit size={18} />
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              <Trash2 size={18} />
              Delete
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-navy-900 mb-4">Patient Information</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Full Name</p>
              <p className="text-lg font-medium text-navy-900">{patient.full_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Date of Birth</p>
              <p className="text-lg font-medium text-navy-900">{patient.date_of_birth}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="text-lg font-medium text-navy-900">{patient.email}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-navy-900 mb-4">Blood Test Values</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Glucose</p>
              <p className="text-lg font-medium text-navy-900">{patient.glucose}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Haemoglobin</p>
              <p className="text-lg font-medium text-navy-900">{patient.haemoglobin}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Cholesterol</p>
              <p className="text-lg font-medium text-navy-900">{patient.cholesterol}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-navy-900">AI Analysis</h3>
            <div className="flex items-center gap-3">
              <StatusBadge status={patient.ai_status} />
              {(patient.ai_status === 'failed' || patient.ai_status === 'unavailable') && (
                <button
                  onClick={handleRetryAI}
                  disabled={retrying}
                  className="flex items-center gap-2 px-3 py-1 text-sm bg-teal-600 text-white rounded hover:bg-teal-700 disabled:opacity-50"
                >
                  <RefreshCw size={16} />
                  {retrying ? 'Retrying...' : 'Retry'}
                </button>
              )}
            </div>
          </div>
          {patient.remarks ? (
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 whitespace-pre-wrap">{patient.remarks}</p>
            </div>
          ) : (
            <div className="bg-gray-50 rounded-lg p-4 text-gray-500">
              {patient.ai_status === 'pending' ? 'AI analysis in progress...' : 'No AI remarks available'}
            </div>
          )}
          <p className="text-xs text-gray-500 mt-4 italic">
            AI-generated information is for demonstration and general awareness only. 
            It is not a medical diagnosis or a substitute for advice from a qualified healthcare professional.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 lg:col-span-2">
          <h3 className="text-lg font-semibold text-navy-900 mb-4">Record Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Created At</p>
              <p className="text-sm text-navy-900">{new Date(patient.created_at).toLocaleString()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Last Updated</p>
              <p className="text-sm text-navy-900">
                {patient.updated_at ? new Date(patient.updated_at).toLocaleString() : 'Never'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientDetails;
