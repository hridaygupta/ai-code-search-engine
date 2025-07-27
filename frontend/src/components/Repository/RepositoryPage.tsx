import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Plus, GitBranch } from 'lucide-react';
import { getRepositories, indexRepository, deleteRepository } from '../../services/api';
import RepositoryCard from './RepositoryCard';
import AddRepositoryModal from './AddRepositoryModal';

const RepositoryPage: React.FC = () => {
  const [showAddModal, setShowAddModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: repositories, isLoading, error } = useQuery(
    'repositories',
    () => getRepositories(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const indexMutation = useMutation(indexRepository, {
    onSuccess: () => {
      queryClient.invalidateQueries('repositories');
      setShowAddModal(false);
    },
  });

  const deleteMutation = useMutation(deleteRepository, {
    onSuccess: () => {
      queryClient.invalidateQueries('repositories');
    },
  });

  const handleAddRepository = (repository: { name: string; url: string; type: string }) => {
    // Transform the data to match the API expectation
    const data = {
      repository_url: repository.url,
      branch: 'main',
      include_patterns: ['**/*.py', '**/*.js', '**/*.ts', '**/*.java', '**/*.cpp', '**/*.go'],
      exclude_patterns: ['**/node_modules/**', '**/__pycache__/**', '**/.git/**'],
    };
    indexMutation.mutate(data);
  };

  const handleDeleteRepository = (repositoryId: string) => {
    if (window.confirm('Are you sure you want to delete this repository?')) {
      deleteMutation.mutate(repositoryId);
    }
  };

  const getStatusStats = () => {
    if (!repositories) return { indexed: 0, indexing: 0, failed: 0 };
    
    return repositories.repositories.reduce((stats: any, repo: any) => {
      stats[repo.status] = (stats[repo.status] || 0) + 1;
      return stats;
    }, {});
  };

  const statusStats = getStatusStats();

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Error Loading Repositories
          </h2>
          <p className="text-gray-600">
            Failed to load repositories. Please try again.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Repositories
          </h1>
          <p className="text-gray-600">
            Manage your indexed code repositories for semantic search
          </p>
        </div>
        
        <button
          onClick={() => setShowAddModal(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Repository</span>
        </button>
      </div>

      {/* Status Overview */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="card text-center">
          <div className="text-2xl font-bold text-blue-600 mb-2">
            {repositories?.repositories.length || 0}
          </div>
          <div className="text-sm text-gray-600">Total Repositories</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-600 mb-2">
            {statusStats.indexed || 0}
          </div>
          <div className="text-sm text-gray-600">Indexed</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-yellow-600 mb-2">
            {statusStats.indexing || 0}
          </div>
          <div className="text-sm text-gray-600">Indexing</div>
        </div>
        
        <div className="card text-center">
          <div className="text-2xl font-bold text-red-600 mb-2">
            {statusStats.failed || 0}
          </div>
          <div className="text-sm text-gray-600">Failed</div>
        </div>
      </div>

      {/* Repositories List */}
      {isLoading ? (
        <div className="card text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading repositories...</p>
        </div>
      ) : repositories?.repositories.length === 0 ? (
        <div className="card text-center py-12">
          <GitBranch className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No repositories yet
          </h3>
          <p className="text-gray-600 mb-6">
            Add your first repository to start indexing code for semantic search.
          </p>
          <button
            onClick={() => setShowAddModal(true)}
            className="btn-primary"
          >
            Add Your First Repository
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {repositories?.repositories.map((repository: any) => (
            <RepositoryCard
              key={repository.id}
              repository={repository}
              onDelete={handleDeleteRepository}
              onView={(id: string) => console.log('View repository:', id)}
              onSettings={(id: string) => console.log('Settings for repository:', id)}
            />
          ))}
        </div>
      )}

      {/* Add Repository Modal */}
      {showAddModal && (
        <AddRepositoryModal
          isOpen={showAddModal}
          onClose={() => setShowAddModal(false)}
          onAdd={handleAddRepository}
        />
      )}
    </div>
  );
};

export default RepositoryPage; 