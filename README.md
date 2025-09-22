# Exam Platform Service

## Overview

The Exam Platform Service is a scalable, containerized web application designed to manage online exams for students and educators. It supports exam creation, student authentication, answer submission, automated grading, and result export, leveraging Django, Express.js, Celery, Cassandra, PostgreSQL, Redis, and a load balancer for fault tolerance.

## Visual Resources

- [Database Schema](https://drawsql.app/teams/test-1748/diagrams/exam-platform)

- [System Design](https://miro.com/app/board/uXjVJQyAWU4=/?share_link_id=638336235797)

## Features

- **User Management:**  
  - Custom user models for Students and Doctors (educators).
  - JWT-based authentication and login endpoints.
  - Permissions for student-only access to exam endpoints.

- **Exam Management:**  
  - Create, list, and retrieve exams.
  - Exams are associated with levels and educators.
  - Questions with multiple choices and optional images.

- **Answer Submission & Grading:**  
  - Students submit answers via FastAPI endpoints.
  - Answers are stored in Cassandra for scalability.
  - Automated grading via Celery tasks, updating scores in PostgreSQL.

- **Admin Interface:**  
  - Django admin for managing users, exams, questions, and student degrees.
  - Import/export functionality for student results.

- **Caching:**  
  - Exam and question data cached for fast retrieval.

- **Load Balancing & Fault Tolerance:**  
  - Requests are distributed across multiple service instances using a load balancer.
  - Ensures high availability and fault tolerance.

- **Testing:**  
  - Comprehensive unit tests for authentication, exam retrieval, listing, and grading.

## Architecture

- **Django:**  
  - Handles user management, exam/question CRUD, and admin interface.
  - REST API endpoints for authentication and exam access.

- **Express.js:**  
  - Save student answer submissions via Cassandra DB.
  - Middleware for JWT authentication.
  - Communicates with Django for token verification.

- **Celery:**  
  - Background task processing for automated grading.

- **Cassandra:**  
  - Stores student answers for high write throughput.

- **PostgreSQL:**  
  - Stores core relational data (users, exams, degrees).

- **Redis:**  
  - Used for caching and as a Celery broker.

- **Nginx:**  
  - Reverse proxy for Django and FastAPI services.

  - Distributes incoming traffic to fastapi service for fault tolerance and scalability.

- **Docker:**  
  - Dockerize all services on the project.

## Directory Structure

- `core/`  
  - Django project with apps: `users`, `exam`, `globals`.
  - Celery configuration and management scripts.

- `exam_expressjs/`  
  - express app for answer submission and authentication middleware.

- `cassandra_orm/`  
  - Custom ORM for Cassandra models and operations.

- `nginx.conf`  
  - Nginx configuration for routing requests.

- `docker-compose.yml`  
  - Multi-service orchestration.

## How It Works

1. **User Authentication:**  
   - Students and doctors log in via Django endpoints.
   - JWT tokens are issued for authenticated requests.

2. **Exam Participation:**  
   - Students retrieve available exams and questions.
   - Submit answers via FastAPI, which stores them in Cassandra.

3. **Grading:**  
   - When an exam is marked for solving, a Celery task fetches answers from Cassandra, grades them, and updates student degrees in PostgreSQL.

4. **Admin Operations:**  
   - Admins can manage users, exams, and export/import results via Django admin.

## Setup & Deployment

1. **Clone the repository.**
2. **Configure environment variables in `.env`.**
3. **Run `docker-compose up --build` to start all services.**
4. **Access Django admin at `localhost/admin/`.**
5. **FastAPI endpoints available at `localhost/solver`.**


## Testing

**For Testing The System**
```
docker container exec -it <DJANGO_CONTAINER_ID> python manage.py test
```

**For Testing Traffic**
```
python test_traffic
```

## Technologies Used

- Django 5.2.5
- Express.js
- Celery
- Cassandra
- PostgreSQL
- Redis
- Nginx
- Docker

## License

MIT License. See [LICENSE](LICENSE) for details.
