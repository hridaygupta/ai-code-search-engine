import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  BarChart3, 
  TrendingUp, 
  Search, 
  GitBranch, 
  Users, 
  Clock,
  Calendar,
  Filter
} from 'lucide-react';
import { getSearchAnalytics, getSearchTrends } from '../../services/api';
import SearchTrendsChart from './SearchTrendsChart';
import PopularQueriesChart from './PopularQueriesChart';
import LanguageDistributionChart from './LanguageDistributionChart';

const AnalyticsPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState('7'); // days

  const { data: analytics, isLoading: analyticsLoading } = useQuery(
    ['analytics', timeRange],
    () => getSearchAnalytics({ days: parseInt(timeRange) }),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const { data: trends, isLoading: trendsLoading } = useQuery(
    ['trends', timeRange],
    () => getSearchTrends(parseInt(timeRange)),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const isLoading = analyticsLoading || trendsLoading;

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };



  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="card text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
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
            Analytics Dashboard
          </h1>
          <p className="text-gray-600">
            Insights into search patterns and repository usage
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="1">Last 24 hours</option>
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
            </select>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Searches</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(analytics?.total_searches || 0)}
              </p>
              <p className={`text-sm ${analytics?.search_growth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {analytics?.search_growth >= 0 ? '+' : ''}{analytics?.search_growth?.toFixed(1)}% from last period
              </p>
            </div>
            <Search className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Unique Users</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(analytics?.unique_users || 0)}
              </p>
              <p className={`text-sm ${analytics?.user_growth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {analytics?.user_growth >= 0 ? '+' : ''}{analytics?.user_growth?.toFixed(1)}% from last period
              </p>
            </div>
            <Users className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Indexed Repositories</p>
              <p className="text-2xl font-bold text-gray-900">
                {formatNumber(analytics?.indexed_repositories || 0)}
              </p>
              <p className={`text-sm ${analytics?.repository_growth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {analytics?.repository_growth >= 0 ? '+' : ''}{analytics?.repository_growth?.toFixed(1)}% from last period
              </p>
            </div>
            <GitBranch className="h-8 w-8 text-purple-600" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg. Response Time</p>
              <p className="text-2xl font-bold text-gray-900">
                {analytics?.avg_response_time?.toFixed(0) || 0}ms
              </p>
              <p className={`text-sm ${analytics?.response_time_change <= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {analytics?.response_time_change <= 0 ? '-' : '+'}{Math.abs(analytics?.response_time_change || 0).toFixed(1)}% from last period
              </p>
            </div>
            <Clock className="h-8 w-8 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid lg:grid-cols-2 gap-8 mb-8">
        {/* Search Trends */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Search Trends</h3>
            <TrendingUp className="h-5 w-5 text-blue-600" />
          </div>
          <SearchTrendsChart data={trends?.daily_searches || []} />
        </div>

        {/* Popular Queries */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Popular Queries</h3>
            <BarChart3 className="h-5 w-5 text-green-600" />
          </div>
          <PopularQueriesChart data={trends?.popular_queries || []} />
        </div>
      </div>

      {/* Language Distribution */}
      <div className="card mb-8">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Language Distribution</h3>
          <Filter className="h-5 w-5 text-purple-600" />
        </div>
        <LanguageDistributionChart data={trends?.popular_languages || []} />
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-6">Recent Activity</h3>
        <div className="space-y-4">
          {analytics?.recent_activity?.map((activity: any, index: number) => (
            <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Search className="h-4 w-4 text-blue-600" />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">
                  {activity.description}
                </p>
                <p className="text-xs text-gray-500">
                  {new Date(activity.timestamp).toLocaleString()}
                </p>
              </div>
              <div className="text-sm text-gray-500">
                {activity.count} searches
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage; 