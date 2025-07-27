import React from 'react';
import { X } from 'lucide-react';

interface SearchFiltersProps {
  filters: {
    languages: string[];
    repositories: string[];
    complexity: string;
    quality: string;
  };
  onFiltersChange: (filters: any) => void;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({ filters, onFiltersChange }) => {
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
    { value: 'excellent', label: 'Excellent' },
    { value: 'good', label: 'Good' },
    { value: 'fair', label: 'Fair' },
    { value: 'poor', label: 'Poor' },
  ];

  const handleLanguageToggle = (language: string) => {
    const newLanguages = filters.languages.includes(language)
      ? filters.languages.filter(l => l !== language)
      : [...filters.languages, language];
    
    onFiltersChange({ ...filters, languages: newLanguages });
  };

  const handleComplexityChange = (complexity: string) => {
    onFiltersChange({ ...filters, complexity });
  };

  const handleQualityChange = (quality: string) => {
    onFiltersChange({ ...filters, quality });
  };

  const clearAllFilters = () => {
    onFiltersChange({
      languages: [],
      repositories: [],
      complexity: 'all',
      quality: 'all',
    });
  };

  const hasActiveFilters = filters.languages.length > 0 || 
                          filters.complexity !== 'all' || 
                          filters.quality !== 'all';

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Search Filters</h3>
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

      {/* Languages */}
      <div className="mb-6">
        <h4 className="font-medium text-gray-900 mb-3">Programming Languages</h4>
        <div className="flex flex-wrap gap-2">
          {languages.map((language) => (
            <button
              key={language}
              onClick={() => handleLanguageToggle(language)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                filters.languages.includes(language)
                  ? 'bg-blue-100 text-blue-700 border border-blue-200'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {language}
            </button>
          ))}
        </div>
      </div>

      {/* Complexity and Quality */}
      <div className="grid md:grid-cols-2 gap-6">
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Code Complexity</h4>
          <select
            value={filters.complexity}
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

        <div>
          <h4 className="font-medium text-gray-900 mb-3">Code Quality</h4>
          <select
            value={filters.quality}
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
            {filters.languages.map((language) => (
              <span
                key={language}
                className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-700"
              >
                {language}
                <button
                  onClick={() => handleLanguageToggle(language)}
                  className="ml-1 hover:text-blue-900"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            ))}
            {filters.complexity !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-700">
                Complexity: {complexityLevels.find(l => l.value === filters.complexity)?.label}
                <button
                  onClick={() => handleComplexityChange('all')}
                  className="ml-1 hover:text-green-900"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            )}
            {filters.quality !== 'all' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-700">
                Quality: {qualityLevels.find(l => l.value === filters.quality)?.label}
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

export default SearchFilters; 