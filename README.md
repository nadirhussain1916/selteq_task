# Selteq Task - Task Management API

A Django REST API project with JWT authentication, Microsoft SQL Server integration, and Celery-based task scheduling.

## Requirements Fulfilled ✓

1. **Django Project Setup**
   - Python 3.9
   - Django REST Framework
   - Project name: selteq_task

2. **Database Integration**
   - Microsoft SQL Server
   - ODBC Driver 17 for SQL Server

3. **Authentication & Authorization**
   - JWT-based authentication
   - Token expiration after 5 minutes
   - Secure endpoints with user-specific access

4. **API Endpoints**
   - POST /api/tasks/ - Create new task with title and duration
   - GET /api/tasks/ - List last 4 tasks of logged-in user
   - GET /api/tasks/{id}/ - Retrieve specific task (using raw SQL)
   - PUT /api/tasks/{id}/ - Update task title only (using raw SQL)
   - DELETE /api/tasks/{id}/ - Delete own tasks

5. **Custom Management Command**
   - Command to print tasks every 10 seconds
   - Uses logging instead of print statements

6. **Celery Integration**
   - Redis as message broker
   - Scheduled task execution
   - Prints tasks for user with ID 1 every minute

## Prerequisites

- Python 3.9
- Docker and Docker Compose
- Microsoft SQL Server ODBC Driver 17

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd selteq_task
   ```

2. **Environment Setup**
   - Ensure Docker and Docker Compose are installed
   - Make sure you have the ODBC Driver 17 for SQL Server installed

3. **Build and Run with Docker**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - Django application on port 8000
   - SQL Server on port 1433
   - Redis on port 6379
   - Celery worker
   - Celery beat scheduler

4. **Create a superuser (in a new terminal)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## API Usage

1. **Obtain JWT Token**
   ```bash
   curl -X POST http://localhost:8000/api/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Create a Task**
   ```bash
   curl -X POST http://localhost:8000/api/tasks/ \
        -H "Authorization: Bearer your_token" \
        -H "Content-Type: application/json" \
        -d '{"title": "Sample Task", "duration": 30}'
   ```

3. **Get User's Tasks**
   ```bash
   curl -X GET http://localhost:8000/api/tasks/ \
        -H "Authorization: Bearer your_token"
   ```

## Project Structure

```
selteq_task/
├── docker-compose.yml    # Docker services configuration
├── Dockerfile           # Django application container
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── selteq_task/       # Main project directory
└── tasks/             # Tasks application
    ├── management/    # Custom management commands
    ├── migrations/    # Database migrations
    └── views.py       # API endpoints
```

## Features

1. **JWT Authentication**
   - Secure token-based authentication
   - 5-minute token expiration
   - Protected API endpoints

2. **Task Management**
   - Create tasks with title and duration
   - View last 4 tasks
   - Update task titles
   - Delete own tasks
   - Raw SQL query implementations

3. **Background Tasks**
   - Celery integration with Redis
   - Scheduled task printing
   - Custom management command for task monitoring

4. **Database**
   - Microsoft SQL Server integration
   - Efficient query handling
   - Secure data access

## Development Approach

### Architecture Decisions
- Chose Django REST Framework for robust API development
- Implemented JWT for stateless authentication
- Used Microsoft SQL Server for enterprise-grade database management
- Integrated Celery with Redis for reliable background task processing
- Implemented Docker for consistent development and deployment environments

### Code Quality Measures
- Comprehensive test coverage for all endpoints
- Raw SQL queries optimized for performance where required
- Proper error handling and validation
- Secure authentication implementation
- Clean code structure following Django best practices

### Security Considerations
- JWT token with short expiration time (5 minutes)
- User-specific data access controls
- SQL injection prevention
- Secure password handling
- Protected API endpoints

### Future Improvements
- Add API documentation using Swagger/OpenAPI
- Implement rate limiting for API endpoints
- Add refresh token mechanism
- Enhanced logging and monitoring
- Add CI/CD pipeline configuration

## Project Submission Notes

This project was developed as part of the technical assessment for the Python Developer position. Key highlights:

1. **Requirements Coverage**
   - All specified requirements have been implemented
   - Added comprehensive test cases
   - Included proper documentation

2. **Technical Stack**
   - Python 3.9
   - Django REST Framework
   - Microsoft SQL Server
   - Redis
   - Celery
   - Docker

3. **Running the Project**
   Follow the setup instructions in the Prerequisites and Setup sections above. For any questions or clarifications, please feel free to reach out.

## Running Tests

```bash
docker-compose exec web python manage.py test
```

## Monitoring

- Celery tasks can be monitored through the container logs
- Database operations are logged in the application logs
- Custom command output is available in tasks.log

## Notes

- The JWT token expires after 5 minutes for security
- Only the last 4 tasks are shown in the task list endpoint
- Task duration cannot be updated after creation
- Raw SQL queries are used for certain endpoints as per requirements
- The Celery beat scheduler prints tasks for user ID 1 every minute

## Error Handling

- Proper error responses for invalid requests
- Authentication failure handling
- Database error management
- Task not found scenarios

## Security Features

- JWT token authentication
- User-specific data access
- SQL injection prevention
- Secure password handling
- Protected API endpoints