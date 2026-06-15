

## Live Deployment

| Component | URL |
|-----------|-----|
| **Live API** | https://tackmaster-api.onrender.com |
| **API Root** | https://tackmaster-api.onrender.com/api/ |
| **Admin Panel** | https://tackmaster-api.onrender.com/admin/ |
| ** Video** | https://web.descript.com/006ed8a0-82d4-46ef-8046-d4e12a12dad7/a8891

## Project Overview

RESTful Task Management API built with Django REST Framework. Features JWT authentication and full CRUD operations for tasks.

### Technology Stack

| Technology | Version |
|------------|---------|
| Django | 4.2.0 |
| Django REST Framework | 3.14.0 |
| SimpleJWT | 5.3.0 |
| PostgreSQL | Render managed |
| Gunicorn | 21.2.0 |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Create new user account |
| POST | `/api/login/` | Login (returns JWT access/refresh tokens) |
| POST | `/api/refresh/` | Refresh expired access token |
| GET | `/api/me/` | Get current user profile |

### Tasks (CRUD)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks/` | List all tasks for logged-in user | ✅ Bearer Token |
| POST | `/api/tasks/` | Create a new task | ✅ Bearer Token |
| GET | `/api/tasks/{id}/` | Get specific task details | ✅ Bearer Token |
| PUT/PATCH | `/api/tasks/{id}/` | Update a task | ✅ Bearer Token |
| DELETE | `/api/tasks/{id}/` | Delete a task | ✅ Bearer Token |

---

## Local Development Setup

### Prerequisites

- Python 3.12+
- pip
- Virtual environment (venv)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/bluTru3/backend_taskmanager.git
cd backend_taskmanager/fresh_taskmanager

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start development server
python manage.py runserver
