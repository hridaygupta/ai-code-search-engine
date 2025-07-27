import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SearchTrendsChartProps {
  data: Array<{
    date: string;
    searches: number;
    uniqueUsers: number;
  }>;
}

const SearchTrendsChart: React.FC<SearchTrendsChartProps> = ({ data }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Search Trends</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="searches" 
            stroke="#3b82f6" 
            strokeWidth={2}
            name="Total Searches"
          />
          <Line 
            type="monotone" 
            dataKey="uniqueUsers" 
            stroke="#10b981" 
            strokeWidth={2}
            name="Unique Users"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SearchTrendsChart; 