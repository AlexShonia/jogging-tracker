# Jogging Tracker

## 🏃‍♂️ Project Overview

Jogging Tracker is an API that demonstrates my ability to build scalable, secure, and feature-rich REST APIs using modern technologies. This project showcases my expertise in backend development, system architecture, and best practices in software engineering.

## 🚀 Key Technical Achievements

### Architecture & Infrastructure
- Implemented a containerized application using Docker for consistent development and deployment
- Set up a robust development environment with PostgreSQL, Redis, and Celery
- Designed a scalable database schema with proper relationships and constraints
- Integrated Redis for message queuing
- Implemented Celery for handling asynchronous tasks and background jobs

### Security & Authentication
- Implemented JWT-based authentication system
- Created role-based access control (RBAC) for different user types
- Secured API endpoints with proper authentication and authorization
- Implemented password hashing and secure user management

### API Design & Implementation
- Built a RESTful API following best practices and standards
- Implemented comprehensive input validation and error handling
- Created efficient ORM queries
- Integrated third-party weather API for real-time weather data
- Implemented weekly report generation with data aggregation

### Performance & Scalability
- Used Celery background tasks for heavy computations
- Optimized ORM queries for better performance

## 🛠️ Technical Stack

### Backend
- **Framework**: Django
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Cache & Message Broker**: Redis
- **Task Queue**: Celery

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git
- **Environment Management**: Python virtual environments

## 💡 Learning Outcomes

This project helped me develop and demonstrate several key skills:

1. **System Design**
   - Containerized application architecture
   - Database design and optimization
   - API design and documentation
   - Security best practices

2. **Technical Skills**
   - Django REST Framework
   - PostgreSQL database management
   - Celery task queue management
   - Docker containerization

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd jogging-tracker
   ```

2. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. Start the application:
   ```bash
   docker-compose up --build
   ```

## 📝 API Documentation

The API provides the following main endpoints:

- **Authentication**
  - User registration and login
  - JWT token management

- **Jogging Activities**
  - CRUD operations for jogging records
  - Weather data integration
  - Location tracking

- **Reports**
  - Weekly activity summaries
  - Performance metrics
  - Statistical analysis

## 📫 Contact

Feel free to reach out to me for any questions or opportunities:
- Email: alex.shonia123@gmail.com
