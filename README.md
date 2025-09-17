# Exam Platform Service

## Overview

The Exam Platform Service is a scalable, containerized web application designed to manage online exams for students and educators. It supports exam creation, student authentication, answer submission, automated grading, and result export, leveraging Django, FastAPI, Celery, Cassandra, PostgreSQL, and Redis.

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

- **Testing:**  
  - Comprehensive unit tests for authentication, exam retrieval, listing, and grading.

## Architecture

- **Django:**  
  - Handles user management, exam/question CRUD, and admin interface.
  - REST API endpoints for authentication and exam access.

- **FastAPI:**  
  - Handles student answer submissions.
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

- **Docker Compose:**  
  - Orchestrates all services for local development and deployment.

## Directory Structure

- `core/`  
  - Django project with apps: `users`, `exam`, `globals`.
  - Celery configuration and management scripts.

- `exam_fastapi/`  
  - FastAPI app for answer submission and authentication middleware.

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
5. **FastAPI endpoints available at `solver.localhost/`.**

## Technologies Used

- Django 5.2.5
- FastAPI
- Celery
- Cassandra
- PostgreSQL
- Redis
- Nginx
- Docker

## License

MIT License. See [LICENSE](LICENSE) for details.

---

For API documentation and usage examples, see the code in [core/users/apis/urls.py](core/users/apis/urls.py), [core/exam/apis/urls.py](core/exam/apis/urls.py), and [exam_fastapi/apis.py](exam_fastapi/apis.py).