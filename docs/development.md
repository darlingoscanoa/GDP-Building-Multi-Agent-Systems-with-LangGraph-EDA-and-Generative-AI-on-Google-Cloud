# Development Guide

This guide provides instructions for setting up and developing the AiDemy platform. This is an enhanced version of the original Google Codelab project with additional development tools and practices.

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Docker and Docker Compose
- Google Cloud SDK
- Git

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd aidemy-bootstrap
   ```

2. **Set Up Python Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project [YOUR_PROJECT_ID]
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Project Structure

```
aidemy-bootstrap/
├── portal/           # Main web interface
├── planner/          # Curriculum planning service
├── courses/          # Course content management
├── assignment/       # Assignment handling
├── bookprovider/     # Book recommendations
├── setup/           # Setup scripts
├── docs/            # Documentation
├── tests/           # Test files
├── scripts/         # Utility scripts
└── config/          # Configuration files
```

## Development Workflow

### 1. Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small

### 2. Testing
- Write unit tests for new features
- Run tests before committing:
  ```bash
  pytest tests/
  ```

### 3. Git Workflow
- Create feature branches
- Write descriptive commit messages
- Keep commits atomic
- Review code before merging

### 4. Documentation
- Update relevant documentation
- Add comments for complex logic
- Keep README up to date

## Running Services Locally

### Portal Service
```bash
cd portal
python app.py
```

### Planner Service
```bash
cd planner
python app.py
```

### Other Services
Each service can be run similarly using its respective app.py file.

## Debugging

### Logging
- Use the logging module
- Set appropriate log levels
- Include context in log messages

### Testing
- Use pytest for unit tests
- Use pytest-cov for coverage
- Write integration tests for critical paths

## Deployment

### Local Deployment
```bash
docker-compose up --build
```

### Cloud Deployment
```bash
./scripts/deploy.sh
```

## Common Issues and Solutions

1. **Authentication Issues**
   - Verify Google Cloud credentials
   - Check service account permissions
   - Ensure environment variables are set

2. **Database Connection**
   - Verify database credentials
   - Check network connectivity
   - Ensure database is running

3. **API Rate Limits**
   - Implement proper rate limiting
   - Use caching where appropriate
   - Monitor API usage

## Best Practices

1. **Code Organization**
   - Keep related code together
   - Use meaningful names
   - Follow consistent patterns

2. **Error Handling**
   - Use try-except blocks
   - Log errors appropriately
   - Provide meaningful error messages

3. **Security**
   - Never commit sensitive data
   - Use environment variables
   - Implement proper authentication

4. **Performance**
   - Optimize database queries
   - Use caching
   - Monitor resource usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Resources

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [LangChain Documentation](https://python.langchain.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Best Practices](https://docs.python-guide.org/) 