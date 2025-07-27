import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { 
  Star, 
  Eye, 
  GitBranch, 
  Calendar, 
  FileText, 
  Code, 
  Copy, 
  ExternalLink,
  ThumbsUp,
  MessageCircle,
  Bookmark
} from 'lucide-react';

interface CodeSnippetProps {
  snippet: {
    id: string;
    title: string;
    content: string;
    language: string;
    repository: {
      name: string;
      url: string;
      owner: string;
    };
    file_path: string;
    line_start: number;
    line_end: number;
    complexity: string;
    quality_score: number;
    stars: number;
    views: number;
    created_at: string;
    updated_at: string;
    tags: string[];
    description?: string;
  };
}

const CodeSnippet: React.FC<CodeSnippetProps> = ({ snippet }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(snippet.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const getLanguageExtension = (language: string) => {
    const extensions: { [key: string]: string } = {
      'python': 'py',
      'javascript': 'js',
      'typescript': 'ts',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'go': 'go',
      'rust': 'rs',
      'php': 'php',
      'ruby': 'rb',
      'csharp': 'cs',
    };
    return extensions[language.toLowerCase()] || language.toLowerCase();
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getComplexityColor = (complexity: string) => {
    const colors = {
      'low': 'bg-green-100 text-green-700',
      'medium': 'bg-yellow-100 text-yellow-700',
      'high': 'bg-orange-100 text-orange-700',
      'very_high': 'bg-red-100 text-red-700',
    };
    return colors[complexity as keyof typeof colors] || 'bg-gray-100 text-gray-700';
  };

  const getQualityColor = (score: number) => {
    if (score >= 8) return 'bg-green-100 text-green-700';
    if (score >= 6) return 'bg-yellow-100 text-yellow-700';
    if (score >= 4) return 'bg-orange-100 text-orange-700';
    return 'bg-red-100 text-red-700';
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {snippet.title}
          </h3>
          {snippet.description && (
            <p className="text-gray-600 text-sm mb-3">
              {snippet.description}
            </p>
          )}
          
          {/* Repository Info */}
          <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
            {snippet.repository && (
              <div className="flex items-center space-x-1">
                <GitBranch className="h-4 w-4" />
                <span>{snippet.repository.owner}/{snippet.repository.name}</span>
              </div>
            )}
            <div className="flex items-center space-x-1">
              <FileText className="h-4 w-4" />
              <span>{snippet.file_path}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Code className="h-4 w-4" />
              <span>Lines {snippet.line_start}-{snippet.line_end}</span>
            </div>
          </div>

          {/* Tags */}
          {snippet.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-3">
              {snippet.tags.map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            title="Copy code"
          >
            <Copy className="h-4 w-4" />
          </button>
          {snippet.repository && (
            <button
              onClick={() => window.open(snippet.repository.url, '_blank')}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="View repository"
            >
              <ExternalLink className="h-4 w-4" />
            </button>
          )}
          <button
            className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
            title="Bookmark"
          >
            <Bookmark className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Code Block */}
      <div className="relative">
        <div className="bg-gray-900 rounded-lg overflow-hidden">
          {/* Code Header */}
          <div className="flex justify-between items-center px-4 py-2 bg-gray-800">
            <div className="flex items-center space-x-2">
              <span className="text-gray-300 text-sm">
                {getLanguageExtension(snippet.language)}
              </span>
              <span className="text-gray-500">•</span>
              <span className="text-gray-300 text-sm">
                {snippet.line_end - snippet.line_start + 1} lines
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 rounded text-xs ${getComplexityColor(snippet.complexity)}`}>
                {snippet.complexity} complexity
              </span>
              <span className={`px-2 py-1 rounded text-xs ${getQualityColor(snippet.quality_score)}`}>
                {snippet.quality_score}/10 quality
              </span>
            </div>
          </div>

          {/* Code Content */}
          <div className={`${!isExpanded && snippet.content.split('\n').length > 20 ? 'max-h-96 overflow-hidden' : ''}`}>
            <SyntaxHighlighter
              language={snippet.language}
              style={tomorrow}
              customStyle={{
                margin: 0,
                padding: '1rem',
                fontSize: '0.875rem',
                lineHeight: '1.5',
              }}
              showLineNumbers
              startingLineNumber={snippet.line_start}
            >
              {snippet.content}
            </SyntaxHighlighter>
          </div>

          {/* Expand/Collapse Button */}
          {snippet.content.split('\n').length > 20 && (
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-gray-900 to-transparent h-12 flex items-end justify-center pb-2">
              <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="px-4 py-1 bg-gray-800 text-gray-300 text-sm rounded hover:bg-gray-700 transition-colors"
              >
                {isExpanded ? 'Show less' : 'Show more'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center space-x-4 text-sm text-gray-500">
          <div className="flex items-center space-x-1">
            <Star className="h-4 w-4" />
            <span>{snippet.stars.toLocaleString()}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Eye className="h-4 w-4" />
            <span>{snippet.views.toLocaleString()}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Calendar className="h-4 w-4" />
            <span>Updated {formatDate(snippet.updated_at)}</span>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button className="flex items-center space-x-1 text-gray-500 hover:text-gray-700 transition-colors">
            <ThumbsUp className="h-4 w-4" />
            <span className="text-sm">Like</span>
          </button>
          <button className="flex items-center space-x-1 text-gray-500 hover:text-gray-700 transition-colors">
            <MessageCircle className="h-4 w-4" />
            <span className="text-sm">Comment</span>
          </button>
        </div>
      </div>

      {/* Copy Success Message */}
      {copied && (
        <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded text-sm">
          Copied!
        </div>
      )}
    </div>
  );
};

export default CodeSnippet; 