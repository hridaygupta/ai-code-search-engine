import React from 'react';
import { X } from 'lucide-react';

interface ResultFiltersProps {
  currentFilters: {
    language?: string;
    complexity?: string;
    quality?: string;
    repositories?: string[];
  };
  onFiltersChange: (filters: any) => void;
}

const ResultFilters: React.FC<ResultFiltersProps> = ({ currentFilters, onFiltersChange }) => {
  const languages = [
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'Go', 'Rust', 'PHP', 'Ruby', 'C#'
  ];

  const complexityLevels = [
    { value: 'all', label: 'All Complexity' },
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'very_high', label: 'Very High' },
  ];

  const qualityLevels = [
    { value: 'all', label: 'All Quality' },
    { value: 'excellent', label: 'Excellent (8-10)' },
    { value: 'good', label: 'Good (6-7)' },
    { value: 'fair', label: 'Fair (4-5)' },
    { value: 'poor', label: 'Poor (1-3)' },
  ];

  const handleLanguageChange = (language: string) => {
    onFiltersChange({ ...currentFilters, language });
  };

  const handleComplexityChange = (complexity: string) => {
    onFiltersChange({ ...currentFilters, complexity });
  };

  const handleQualityChange = (quality: string) => {
    onFiltersChange({ ...currentFilters, quality });
  };

  const clearAllFilters = () => {
    onFiltersChange({
      language: 'all',
      complexity: 'all',
      quality: 'all',
      repositories: [],
    });
  };

  const hasActiveFilters = currentFilters.language !== 'all' || 
                          currentFilters.complexity !== 'all' || 
                          currentFilters.quality !== 'all';

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Filter Results</h3>
        {hasActiveFilters && (
          <button
            onClick={clearAllFilters}
            className="text-sm text-gray-500 hover:text-gray-700 flex items-center space-x-1"
          >
            <X className="h-4 w-4" />
            <span>Clear all</span>
          </button>
        )}
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Language Filter */}
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Programming Language</h4>
          <select
            value={currentFilters.language || 'all'}
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Languages</option>
            {languages.map((language) => (
              <option key={language} value={language.toLowerCase()}>
                {language}
              </option>
            ))}
          </select>
        </div>

        {/* Complexity Filter */}
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Code Complexity</h4>
          <select
            value={currentFilters.complexity || 'all'}
            onChange={(e) => handleComplexityChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {complexityLevels.map((level) => (
              <option key={level.value} value={level.value}>
                {level.label}
              </option>
            ))}
          </select>
        </div>

        {/* Quality Filter */}
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Code Quality</h4>
          <select
            value={currentFilters.quality || 'all'}
            onChange={(e) => handleQualityChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {qualityLevels.map((level) => (
              <option key={level.value} value={level.value}>
                {level.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Active Filters Summary */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h4 className="font-medium text-gray-900 mb-2">Active Filters:</h4>
          <div className="flex flex-wrap gap-2">
            {currentFilters.language && currentFilters.language !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-700">
                Language: {currentFilters.language}
                <button
                  onClick={() => handleLanguageChange('all')}
                  className="ml-1 hover:text-blue-900"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            )}
            {currentFilters.complexity && currentFilters.complexity !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-700">
                Complexity: {complexityLevels.find(l => l.value === currentFilters.complexity)?.label}
                <button
                  onClick={() => handleComplexityChange('all')}
                  className="ml-1 hover:text-green-900"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            )}
            {currentFilters.quality && currentFilters.quality !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-700">
                Quality: {qualityLevels.find(l => l.value === currentFilters.quality)?.label}
                <button
                  onClick={() => handleQualityChange('all')}
                  className="ml-1 hover:text-purple-900"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultFilters; 