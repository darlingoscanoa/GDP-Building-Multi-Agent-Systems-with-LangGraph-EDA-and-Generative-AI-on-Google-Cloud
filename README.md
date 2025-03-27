# AiDemy Bootstrap

AiDemy is a comprehensive educational platform that demonstrates the power of multi-agent systems and AI in education. Built on Google Cloud and leveraging Gemini models, it showcases how complex AI applications can enhance the learning experience.

## 🌟 Features

- **Intelligent Course Planning**: AI-powered curriculum generation and management
- **Interactive Learning**: Dynamic quiz system with adaptive difficulty
- **Smart Assessment**: Automated answer evaluation with detailed feedback
- **Resource Management**: Integrated book recommendations and course materials
- **Multi-Agent Architecture**: Coordinated AI agents working together

## 🏗️ Project Structure

### Portal (`/portal`)
The main interface for students and educators:
- Course content delivery and management
- Interactive quiz system with adaptive difficulty
- AI-powered answer evaluation and feedback
- Teaching plan generation and management
- Built with Flask, includes modern web interface

### Planner (`/planner`)
Intelligent curriculum planning service:
- AI-driven curriculum generation
- Personalized learning path creation
- Smart content organization
- Integration with educational standards

### Courses (`/courses`)
Course content management system:
- Structured course material storage
- Curriculum organization
- Learning resource management
- Content versioning

### Assignment (`/assignment`)
Advanced assignment handling system:
- Automated assignment creation
- Student submission management
- AI-powered grading system
- Detailed feedback generation

### Book Provider (`/bookprovider`)
Smart book recommendation service:
- AI-driven book recommendations
- Reading level assessment
- Curriculum-aligned suggestions
- Integration with learning paths

### Setup (`/setup`)
Configuration and deployment scripts:
- Environment setup
- Service initialization
- Deployment automation
- Configuration management

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI/ML**: 
  - Google Vertex AI (Gemini models)
  - Langchain for agent orchestration
  - Deepseek
  - Ollama integrations
- **Infrastructure**:
  - Google Cloud Platform
  - Docker for containerization
  - Cloud Storage for content
- **Frontend**:
  - Modern web templates
  - Responsive design
  - Interactive UI components

## 🚀 Getting Started

1. **Prerequisites**:
   - Google Cloud Platform account
   - Docker installed
   - Python 3.8+

2. **Setup**:
   ```bash
   # Clone the repository
   git clone [repository-url]
   
   # Navigate to setup directory
   cd setup
   
   # Run setup script
   ./setup.sh
   ```

3. **Configuration**:
   - Set up Google Cloud credentials
   - Configure environment variables
   - Initialize services

4. **Running the Application**:
   ```bash
   # Start all services
   docker-compose up
   ```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Architecture Overview](docs/architecture.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

While this is a Google-maintained project, we welcome suggestions and improvements. Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 License

This project is maintained by Google. All rights reserved.

## 🙏 Acknowledgments

- Google Cloud Platform team
- Langchain community
- All contributors and maintainers

## 🔄 Updates and Maintenance

This repository is actively maintained and updated with:
- Latest AI model integrations
- Security patches
- Performance improvements
- New features and capabilities
