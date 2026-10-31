import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save } from 'lucide-react';
import ErrorMessage from '../components/ErrorMessage';
import { patientApi } from '../services/patientApi';

const AddPatient = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    full_name: '',
    date_of_birth: '',
    email: '',
    glucose: '',
    haemoglobin: '',
    cholesterol: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const payload = {
        ...formData,
        glucose: parseFloat(formData.glucose),
        haemoglobin: parseFloat(formData.haemoglobin),
        cholesterol: parseFloat(formData.cholesterol),
      };
      await patientApi.create(payload);
      navigate('/patients');
    } catch (err) {
      setError(err.message || 'Failed to create patient record');
    } finally {
      setLoading(false);
    }
  };

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
        <h2 className="text-3xl font-bold text-navy-900">Add Patient</h2>
        <p className="text-gray-600 mt-2">Enter patient information and blood test values</p>
      </div>

      <div className="max-w-2xl">
        <ErrorMessage message={error} />

        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-navy-900 mb-2">
                Full Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                placeholder="Enter full name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-navy-900 mb-2">
                Date of Birth <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="date_of_birth"
                value={formData.date_of_birth}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                placeholder="dd/mm/yyyy"
              />
              <p className="text-xs text-gray-500 mt-1">Format: dd/mm/yyyy (e.g., 28/01/1960)</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-navy-900 mb-2">
                Email Address <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                placeholder="email@example.com"
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-navy-900 mb-2">
                  Glucose <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  step="any"
                  name="glucose"
                  value={formData.glucose}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-navy-900 mb-2">
                  Haemoglobin <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  step="any"
                  name="haemoglobin"
                  value={formData.haemoglobin}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                  placeholder="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-navy-900 mb-2">
                  Cholesterol <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  step="any"
                  name="cholesterol"
                  value={formData.cholesterol}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
                  placeholder="0"
                />
              </div>
            </div>

            <div className="pt-4">
              <button
                type="submit"
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save size={20} />
                {loading ? 'Creating...' : 'Create Patient'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddPatient;
