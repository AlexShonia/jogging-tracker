# Jogging Tracker

API is live now: http://jog-tracker.ashonia.info

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

### Advanced Filtering System
- Implemented a powerful and flexible filtering system that supports:
  - Multiple filter types: exact match, range, negation, and OR conditions
  - Complex queries combining multiple filters
  - Filtering on all relevant fields (date, distance, time, location, etc.)
  - Support for both jogging activities and weekly reports
  - Efficient database queries with proper indexing

### Comprehensive Test Suite
- Implemented extensive test coverage for all major features
- Tests for user authentication and role-based permissions
- API endpoint testing with REST framework's APIClient
- Data validation and business logic testing
- Weekly report calculation verification
- Test cases for all user roles (admin, manager, customer)

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

### Authentication Endpoints
- `POST /api/token/` - Obtain JWT access and refresh tokens
- `POST /api/token/refresh/` - Refresh JWT access token
- `POST /register/` - Register a new user

### Jogging Activities Endpoints
- `GET /jogs/` - List jogging activities (with filtering)
  - Query Parameters:
    - `date`, `not_date`, `from_date`, `to_date`, `date_or`
    - `distance`, `not_distance`, `from_distance`, `to_distance`, `distance_or`
    - `time`, `not_time`, `from_time`, `to_time`, `time_or`
    - `location`, `not_location`
- `POST /jogs/` - Create a new jogging activity
- `GET /jogs/{id}/` - Retrieve a specific jogging activity
- `PUT /jogs/{id}/` - Update a jogging activity
- `DELETE /jogs/{id}/` - Delete a jogging activity

### User Management Endpoints (Manager/Admin only)
- `GET /users/` - List users (filterable by id, email)
- `GET /users/{id}/` - Retrieve user details
- `PUT /users/{id}/` - Update user details
- `DELETE /users/{id}/` - Delete a user

### Weekly Reports Endpoints
- `GET /weekly-report/` - Get weekly jogging reports
  - Query Parameters:
    - `date`, `not_date`, `from_date`, `to_date`, `date_or`
    - `average_speed`, `not_average_speed`, `from_average_speed`, `to_average_speed`, `average_speed_or`
    - `average_distance`, `not_average_distance`, `from_average_distance`, `to_average_distance`, `average_distance_or`

### Authentication
All endpoints except registration and token obtain/refresh require JWT authentication:
```
Authorization: Bearer <your_access_token>
```

## 📫 Contact

Feel free to reach out to me for any questions or opportunities:
- Email: alex.shonia123@gmail.com
