import React from 'react';
import { TrendingUp, Clock, Star } from 'lucide-react';

interface SearchSuggestionsProps {
  query: string;
  onSuggestionClick: (suggestion: string) => void;
}

const SearchSuggestions: React.FC<SearchSuggestionsProps> = ({ query, onSuggestionClick }) => {
  // Mock data - in real app, this would come from API
  const trendingSearches = [
    { query: 'machine learning algorithms', count: 1250, trend: 'up' },
    { query: 'web development frameworks', count: 980, trend: 'up' },
    { query: 'data structures implementation', count: 750, trend: 'stable' },
    { query: 'sorting algorithms comparison', count: 620, trend: 'down' },
    { query: 'API design patterns', count: 540, trend: 'up' },
  ];

  const recentSearches = [
    'binary search tree',
    'quick sort implementation',
    'react hooks patterns',
    'python decorators',
    'docker containerization',
  ];

  const popularTopics = [
    { topic: 'Algorithms', icon: '🔢', count: 2500 },
    { topic: 'Web Development', icon: '🌐', count: 1800 },
    { topic: 'Machine Learning', icon: '🤖', count: 1200 },
    { topic: 'Data Structures', icon: '📊', count: 900 },
    { topic: 'System Design', icon: '🏗️', count: 700 },
  ];

  if (query.length > 0) {
    return null; // Don't show suggestions when user is typing
  }

  return (
    <div className="grid md:grid-cols-3 gap-6">
      {/* Trending Searches */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <TrendingUp className="h-5 w-5 text-orange-500" />
          <h3 className="text-lg font-semibold text-gray-900">Trending Searches</h3>
        </div>
        <div className="space-y-3">
          {trendingSearches.map((item, index) => (
            <button
              key={index}
              onClick={() => onSuggestionClick(item.query)}
              className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors group"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                    {item.query}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {item.count.toLocaleString()} searches
                  </p>
                </div>
                <div className={`text-xs px-2 py-1 rounded-full ${
                  item.trend === 'up' ? 'bg-green-100 text-green-700' :
                  item.trend === 'down' ? 'bg-red-100 text-red-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {item.trend === 'up' ? '↗' : item.trend === 'down' ? '↘' : '→'}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Searches */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Clock className="h-5 w-5 text-blue-500" />
          <h3 className="text-lg font-semibold text-gray-900">Recent Searches</h3>
        </div>
        <div className="space-y-2">
          {recentSearches.map((search, index) => (
            <button
              key={index}
              onClick={() => onSuggestionClick(search)}
              className="w-full text-left p-2 rounded-lg hover:bg-gray-50 transition-colors text-sm text-gray-700 hover:text-blue-600"
            >
              {search}
            </button>
          ))}
        </div>
      </div>

      {/* Popular Topics */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Star className="h-5 w-5 text-yellow-500" />
          <h3 className="text-lg font-semibold text-gray-900">Popular Topics</h3>
        </div>
        <div className="space-y-3">
          {popularTopics.map((topic, index) => (
            <button
              key={index}
              onClick={() => onSuggestionClick(topic.topic)}
              className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors group"
            >
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{topic.icon}</span>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                    {topic.topic}
                  </p>
                  <p className="text-xs text-gray-500">
                    {topic.count.toLocaleString()} results
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchSuggestions; 