import React from 'react';
import { GitBranch, Eye, Settings, Trash2 } from 'lucide-react';

interface Repository {
  id: string;
  name: string;
  url: string;
  status: 'indexed' | 'indexing' | 'failed';
  lastIndexed?: string;
  fileCount?: number;
  language?: string;
}

interface RepositoryCardProps {
  repository: Repository;
  onDelete: (id: string) => void;
  onView: (id: string) => void;
  onSettings: (id: string) => void;
}

const RepositoryCard: React.FC<RepositoryCardProps> = ({
  repository,
  onDelete,
  onView,
  onSettings,
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'indexed':
        return 'bg-green-100 text-green-800';
      case 'indexing':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'indexed':
        return '✓';
      case 'indexing':
        return '⟳';
      case 'failed':
        return '✗';
      default:
        return '?';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <GitBranch className="w-4 h-4 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900">{repository.name}</h3>
          </div>
          
          <p className="text-sm text-gray-600 mb-3 break-all">{repository.url}</p>
          
          <div className="flex items-center space-x-4 mb-4">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(repository.status)}`}>
              <span className="mr-1">{getStatusIcon(repository.status)}</span>
              {repository.status}
            </span>
            
            {repository.language && (
              <span className="text-sm text-gray-600">
                Language: {repository.language}
              </span>
            )}
            
            {repository.fileCount && (
              <span className="text-sm text-gray-600">
                Files: {repository.fileCount.toLocaleString()}
              </span>
            )}
          </div>
          
          {repository.lastIndexed && (
            <p className="text-xs text-gray-500">
              Last indexed: {new Date(repository.lastIndexed).toLocaleDateString()}
            </p>
          )}
        </div>
        
        <div className="flex space-x-2">
          <button
            onClick={() => onView(repository.id)}
            className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="View repository"
          >
            <Eye className="w-4 h-4" />
          </button>
          
          <button
            onClick={() => onSettings(repository.id)}
            className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
            title="Repository settings"
          >
            <Settings className="w-4 h-4" />
          </button>
          
          <button
            onClick={() => onDelete(repository.id)}
            className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Delete repository"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RepositoryCard; 