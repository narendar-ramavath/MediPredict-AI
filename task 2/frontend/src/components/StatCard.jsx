const StatCard = ({ title, value, icon: Icon, color = 'navy' }) => {
  const colorClasses = {
    navy: 'bg-navy-500',
    teal: 'bg-teal-500',
    blue: 'bg-blue-500',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 font-medium">{title}</p>
          <p className="text-3xl font-bold text-navy-900 mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]} text-white`}>
          <Icon size={24} />
        </div>
      </div>
    </div>
  );
};

export default StatCard;
