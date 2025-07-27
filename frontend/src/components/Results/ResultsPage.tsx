import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import { Filter, Code } from 'lucide-react';
import SearchBar from '../Search/SearchBar';
import CodeSnippet from './CodeSnippet';
import ResultFilters from './ResultFilters';
import { searchCode } from '../../services/api';

const ResultsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [showFilters, setShowFilters] = useState(false);
  
  const query = searchParams.get('q') || '';
  const page = parseInt(searchParams.get('page') || '1');
  const language = searchParams.get('language') || '';
  const complexity = searchParams.get('complexity') || '';

  const { data: searchResults, isLoading, error } = useQuery(
    ['search', query, page, language, complexity],
    () => searchCode({ query, page, language, complexity }),
    {
      enabled: !!query,
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const handleSearch = (newQuery: string) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('q', newQuery);
    newParams.set('page', '1');
    setSearchParams(newParams);
  };

  const handlePageChange = (newPage: number) => {
    const newParams = new URLSearchParams(searchParams);
    newParams.set('page', newPage.toString());
    setSearchParams(newParams);
  };

  const handleFilterChange = (filters: any) => {
    const newParams = new URLSearchParams(searchParams);
    Object.entries(filters).forEach(([key, value]) => {
      if (value && value !== 'all') {
        newParams.set(key, value.toString());
      } else {
        newParams.delete(key);
      }
    });
    newParams.set('page', '1');
    setSearchParams(newParams);
  };

  if (error) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Search Error
          </h2>
          <p className="text-gray-600">
            An error occurred while searching. Please try again.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Search Header */}
      <div className="mb-6">
        <SearchBar
          value={query}
          onChange={() => {}} // Controlled by URL params
          onSearch={handleSearch}
          placeholder="Search for code snippets..."
        />
      </div>

      {/* Results Header */}
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Search Results
          </h1>
          {searchResults && (
            <span className="text-gray-600">
              {searchResults.total_results.toLocaleString()} results
            </span>
          )}
        </div>
        
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <Filter className="h-4 w-4" />
          <span>Filters</span>
        </button>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="mb-6">
          <ResultFilters
            currentFilters={{ language, complexity }}
            onFiltersChange={handleFilterChange}
          />
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="card text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Searching for code snippets...</p>
        </div>
      )}

      {/* Results */}
      {searchResults && !isLoading && (
        <>
          <div className="space-y-6">
            {searchResults.results.map((result: any) => (
              <CodeSnippet key={result.id} snippet={result} />
            ))}
          </div>

          {/* Pagination */}
          {searchResults.total_pages > 1 && (
            <div className="mt-8 flex justify-center">
              <nav className="flex items-center space-x-2">
                <button
                  onClick={() => handlePageChange(page - 1)}
                  disabled={page <= 1}
                  className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                
                {Array.from({ length: Math.min(5, searchResults.total_pages) }, (_, i) => {
                  const pageNum = Math.max(1, Math.min(searchResults.total_pages - 4, page - 2)) + i;
                  return (
                    <button
                      key={pageNum}
                      onClick={() => handlePageChange(pageNum)}
                      className={`px-3 py-2 text-sm font-medium rounded-md ${
                        pageNum === page
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-500 bg-white border border-gray-300 hover:bg-gray-50'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                
                <button
                  onClick={() => handlePageChange(page + 1)}
                  disabled={page >= searchResults.total_pages}
                  className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </nav>
            </div>
          )}
        </>
      )}

      {/* No Results */}
      {searchResults && searchResults.results.length === 0 && !isLoading && (
        <div className="card text-center py-12">
          <Code className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            No results found
          </h3>
          <p className="text-gray-600 mb-4">
            Try adjusting your search terms or filters to find what you're looking for.
          </p>
          <div className="space-y-2">
            <p className="text-sm text-gray-500">Suggestions:</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Check your spelling</li>
              <li>• Try more general keywords</li>
              <li>• Remove some filters</li>
              <li>• Use different programming language terms</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsPage; 