import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Code, Zap } from 'lucide-react';
import SearchBar from './SearchBar';
import SearchFilters from './SearchFilters';
import SearchSuggestions from './SearchSuggestions';

const SearchPage: React.FC = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    languages: [],
    repositories: [],
    complexity: 'all',
    quality: 'all',
  });
  const [showFilters, setShowFilters] = useState(false);

  const handleSearch = (searchQuery: string) => {
    const params = new URLSearchParams();
    params.append('q', searchQuery);
    
    if (filters.languages.length > 0) {
      filters.languages.forEach(lang => params.append('languages', lang));
    }
    if (filters.repositories.length > 0) {
      filters.repositories.forEach(repo => params.append('repositories', repo));
    }
    if (filters.complexity) {
      params.append('complexity', filters.complexity);
    }
    if (filters.quality) {
      params.append('quality', filters.quality);
    }
    
    navigate(`/results?${params.toString()}`);
  };

  const popularSearches = [
    'sorting algorithm',
    'binary search',
    'quick sort',
    'machine learning',
    'web development',
    'data structures',
  ];

  const features = [
    {
      icon: Code,
      title: 'Semantic Search',
      description: 'Find code by understanding its meaning, not just keywords',
    },
    {
      icon: Zap,
      title: 'AI-Powered',
      description: 'Advanced AI models understand code context and relationships',
    },
    {
      icon: Search,
      title: 'Multi-Language',
      description: 'Search across Python, JavaScript, Java, C++, Go, Rust, and more',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI-Powered Code Search
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Find code snippets by understanding their meaning, not just keywords
        </p>
        
        {/* Search Bar */}
        <div className="max-w-3xl mx-auto mb-8">
          <SearchBar
            value={query}
            onChange={setQuery}
            onSearch={handleSearch}
            placeholder="Search for code snippets, functions, algorithms..."
          />
        </div>

        {/* Search Filters Toggle */}
        <div className="flex justify-center mb-6">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <Filter className="h-4 w-4" />
            <span>Advanced Filters</span>
          </button>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="max-w-3xl mx-auto mb-8">
            <SearchFilters
              filters={filters}
              onFiltersChange={setFilters}
            />
          </div>
        )}
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        {features.map((feature, index) => {
          const Icon = feature.icon;
          return (
            <div key={index} className="card text-center">
              <div className="flex justify-center mb-4">
                <Icon className="h-12 w-12 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          );
        })}
      </div>

      {/* Popular Searches */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Popular Searches
        </h2>
        <div className="flex flex-wrap gap-2">
          {popularSearches.map((search, index) => (
            <button
              key={index}
              onClick={() => handleSearch(search)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm transition-colors"
            >
              {search}
            </button>
          ))}
        </div>
      </div>

      {/* Search Suggestions */}
      <div className="mt-8">
        <SearchSuggestions query={query} onSuggestionClick={handleSearch} />
      </div>
    </div>
  );
};

export default SearchPage; 