const StatusBadge = ({ status }) => {
  const statusConfig = {
    pending: { bg: 'bg-yellow-100', text: 'text-yellow-800', label: 'AI Pending' },
    completed: { bg: 'bg-green-100', text: 'text-green-800', label: 'AI Complete' },
    unavailable: { bg: 'bg-gray-100', text: 'text-gray-800', label: 'AI Unavailable' },
    failed: { bg: 'bg-red-100', text: 'text-red-800', label: 'AI Failed' },
  };

  const config = statusConfig[status] || statusConfig.pending;

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
      {config.label}
    </span>
  );
};

export default StatusBadge;
