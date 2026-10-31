import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/patients', label: 'Patients', icon: Users },
  ];

  return (
    <aside className="w-64 bg-navy-900 text-white min-h-screen p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-teal-400">MediPredict AI</h1>
        <p className="text-sm text-gray-400 mt-1">Patient Management</p>
      </div>
      
      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-teal-600 text-white'
                  : 'text-gray-300 hover:bg-navy-800 hover:text-white'
              }`
            }
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
