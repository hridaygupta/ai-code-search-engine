# AI-Powered Contextual Code Search Engine

A sophisticated, AI-powered code search engine that provides semantic understanding and intelligent code discovery across multiple programming languages.

## 🚀 Features

### 🔍 **Intelligent Search**
- **Semantic Code Understanding**: AI-powered search that understands code context and intent
- **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- **Hybrid Search**: Combines semantic similarity with keyword matching
- **Real-time Suggestions**: Intelligent search suggestions and auto-completion
- **Code Highlighting**: Highlighted search matches in results

### 📊 **Advanced Analytics**
- **Search Trends**: Track search patterns and popular queries
- **Language Distribution**: Analyze code distribution across programming languages
- **Repository Insights**: Comprehensive repository analytics and metrics
- **Performance Monitoring**: Real-time system performance tracking

### 🏗️ **Repository Management**
- **Multi-Platform Integration**: GitHub, GitLab, and Bitbucket support
- **Incremental Indexing**: Smart indexing that only processes changed files
- **Branch Support**: Search across different branches and versions
- **Access Control**: Secure repository access with OAuth authentication

### 🤖 **AI-Powered Features**
- **Code Embeddings**: Advanced vector embeddings for semantic similarity
- **Intent Detection**: Understands search intent and context
- **Code Quality Analysis**: Automated code quality scoring and complexity analysis
- **Smart Ranking**: AI-driven result ranking based on relevance and quality

## 🛠️ Technology Stack

### **Backend**
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Primary database for metadata and user management
- **Qdrant**: Vector database for semantic search
- **Neo4j**: Graph database for code relationships
- **Redis**: Caching and session management
- **Elasticsearch**: Full-text search and indexing
- **Celery**: Asynchronous task processing

### **Frontend**
- **React**: Modern UI framework with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Beautiful data visualization
- **Monaco Editor**: Advanced code editor integration
- **Socket.io**: Real-time updates and notifications

### **AI/ML**
- **Transformers**: CodeBERT, GraphCodeBERT, CodeT5 models
- **FAISS**: Efficient similarity search
- **Tree-sitter**: Multi-language parsing
- **Sentence Transformers**: Text embeddings

### **DevOps**
- **Docker**: Containerized deployment
- **Kubernetes**: Orchestration and scaling
- **Prometheus**: Monitoring and alerting
- **Grafana**: Metrics visualization
- **Nginx**: Reverse proxy and load balancing

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### 1. Clone the Repository
```bash
git clone git@github.com:hridaygupta/ai-code-search-engine.git
cd ai-code-search-engine
```

### 2. Start the Application
```bash
# Start all services
docker-compose up -d

# Or start specific services
docker-compose up -d postgres redis elasticsearch neo4j backend
```

### 3. Start Frontend (Development)
```bash
cd frontend
npm install
npm start
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **Elasticsearch**: http://localhost:9200

## 📖 Usage

### Basic Search
1. Navigate to the search page
2. Enter your search query (e.g., "bubble sort algorithm")
3. View real-time results with highlighted matches
4. Filter by programming language or repository

### Advanced Features
- **Language Filtering**: Filter results by specific programming languages
- **Repository Filtering**: Search within specific repositories
- **Complexity Analysis**: View code complexity metrics
- **Quality Scoring**: See AI-generated code quality scores
- **Similar Code**: Find similar code snippets

### Repository Management
1. Add repositories from GitHub, GitLab, or Bitbucket
2. Configure indexing settings
3. Monitor indexing progress
4. View repository analytics

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/codesearch
REDIS_URL=redis://localhost:6379

# AI Models
HUGGINGFACE_TOKEN=your_token_here
MODEL_CACHE_DIR=./ai-models

# Authentication
JWT_SECRET_KEY=your_secret_key
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Search Settings
SIMILARITY_THRESHOLD=0.7
MAX_SEARCH_RESULTS=100
```

### Docker Configuration
The application uses Docker Compose for easy deployment. Key services:

- **Backend**: FastAPI application with all AI models
- **Frontend**: React application with development server
- **Databases**: PostgreSQL, Redis, Elasticsearch, Neo4j
- **Monitoring**: Prometheus and Grafana

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📊 API Documentation

### Search Endpoints
- `GET /api/v1/search/` - Main search endpoint
- `GET /api/v1/search/suggestions` - Search suggestions
- `GET /api/v1/search/similar/{snippet_id}` - Find similar code
- `POST /api/v1/search/explain` - Explain code snippets

### Repository Endpoints
- `GET /api/v1/repositories` - List repositories
- `POST /api/v1/repositories` - Add repository
- `DELETE /api/v1/repositories/{id}` - Remove repository

### Analytics Endpoints
- `GET /api/v1/analytics/search` - Search analytics
- `GET /api/v1/analytics/repositories` - Repository analytics
- `GET /api/v1/analytics/trends` - Search trends

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Write comprehensive tests
- Update documentation for new features

## 📈 Performance

### Search Performance
- **Average Response Time**: < 200ms
- **Concurrent Users**: 1000+
- **Index Size**: Supports millions of code snippets
- **Memory Usage**: Optimized for production deployment

### Scalability
- **Horizontal Scaling**: Kubernetes-ready deployment
- **Load Balancing**: Nginx reverse proxy
- **Caching**: Redis-based caching layer
- **Database Optimization**: Connection pooling and indexing

## 🔒 Security

- **OAuth 2.0**: Secure authentication with GitHub, GitLab, Bitbucket
- **JWT Tokens**: Stateless authentication
- **Rate Limiting**: API rate limiting and protection
- **Input Validation**: Comprehensive input sanitization
- **HTTPS**: Secure communication in production

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing excellent transformer models
- **FastAPI**: For the amazing web framework
- **React**: For the powerful frontend framework
- **Docker**: For containerization technology

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/hridaygupta/ai-code-search-engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hridaygupta/ai-code-search-engine/discussions)
- **Documentation**: [Wiki](https://github.com/hridaygupta/ai-code-search-engine/wiki)

---

**Built with ❤️ for the developer community** 