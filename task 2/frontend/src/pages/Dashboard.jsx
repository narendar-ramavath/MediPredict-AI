import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, Activity, AlertCircle, CheckCircle } from 'lucide-react';
import StatCard from '../components/StatCard';
import { patientApi } from '../services/patientApi';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total: 0,
    recent: 0,
    aiCompleted: 0,
    aiPending: 0,
  });
  const [loading, setLoading] = useState(true);
  const [healthStatus, setHealthStatus] = useState('unknown');

  useEffect(() => {
    loadStats();
    checkHealth();
  }, []);

  const loadStats = async () => {
    try {
      const response = await patientApi.getAll();
      const patients = response.data;
      
      setStats({
        total: patients.length,
        recent: patients.length,
        aiCompleted: patients.filter(p => p.ai_status === 'completed').length,
        aiPending: patients.filter(p => p.ai_status === 'pending').length,
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const checkHealth = async () => {
    try {
      const response = await patientApi.getHealth();
      setHealthStatus(response.data.status);
    } catch (error) {
      setHealthStatus('unhealthy');
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-navy-900">Dashboard</h2>
        <p className="text-gray-600 mt-2">Patient record management overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Patients"
          value={loading ? '-' : stats.total}
          icon={Users}
          color="navy"
        />
        <StatCard
          title="AI Analysis Complete"
          value={loading ? '-' : stats.aiCompleted}
          icon={CheckCircle}
          color="teal"
        />
        <StatCard
          title="AI Analysis Pending"
          value={loading ? '-' : stats.aiPending}
          icon={Activity}
          color="blue"
        />
        <StatCard
          title="System Status"
          value={healthStatus === 'healthy' ? 'OK' : 'Error'}
          icon={AlertCircle}
          color={healthStatus === 'healthy' ? 'teal' : 'red'}
        />
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <h3 className="text-lg font-semibold text-navy-900 mb-4">Welcome to MediPredict AI</h3>
        <div className="space-y-3 text-gray-600">
          <p>• Add patient records with blood test values</p>
          <p>• AI generates informational remarks based on test results</p>
          <p>• View, edit, and manage patient records</p>
          <p className="text-sm text-gray-500 mt-4 italic">
            Note: AI-generated information is for demonstration and general awareness only. 
            It is not a medical diagnosis or a substitute for advice from a qualified healthcare professional.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
