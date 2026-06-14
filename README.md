# Task Manager API - ESE Assignment Final Submission

## Assignment Information

- **Module:** ESE1 - Enterprise Software Engineering
- **Student:** [Your Name]
- **Submission Date:** [Current Date]

---

## Summary

This document describes the development journey of a Task Management REST API built with Django REST Framework. The project encountered significant technical challenges during development, which required a complete restart and restructure. This README documents that investigation process, the lessons learned, and the final working implementation.

**Final Working Code Location:** `/fresh_taskmanager` directory

**Live API:** `https://humble-broccoli-7g94jxrpxvv2x7pv-8000.app.github.dev/`

---

## Development Journey & Investigation

### Phase 1: Initial Project Structure (Failed)

The initial project was created with a nested folder structure:

taskmaster_backend/
└── django_task_manager_backend/
└── backend/
├── backend/ # Nested - caused import issues
├── accounts/
└── tasks/


**Problems Encountered:**

| Problem | Error Message | Root Cause |
|---------|---------------|------------|
| Missing packages | `ModuleNotFoundError: No module named 'dj_database_url'` | Dependencies not installed |
| Missing REST framework | `ModuleNotFoundError: No module named 'rest_framework'` | Django REST Framework missing |
| WSGI configuration | `WSGI application 'backend.wsgi.application' could not be loaded` | Nested folder structure |
| Settings module | `ModuleNotFoundError: No module named 'backend'` | PYTHONPATH pointing to wrong location |

**Investigation Steps Taken:**

1. Attempted to fix by installing missing packages individually
2. Modified `manage.py` and `settings.py` multiple times
3. Attempted to restructure the nested folders
4. Discovered that the nested `backend/backend/` structure was the root cause
5. Spent approximately 4-6 hours debugging import and path issues

**Key Learning:** Django expects a flat project structure or properly configured Python paths. Nested folders with the same name as the project cause circular imports.

### Phase 2: Environment Corruption

During debugging, the Codespace environment became corrupted:

- Virtual environment paths were broken
- PYTHONPATH environment variable pointed to non-existent locations
- Terminal showed `(venv)` but packages weren't accessible
- Multiple attempts to recreate the virtual environment failed

**Investigation Steps:**

1. Checked `which python` - showed system Python, not venv Python
2. Examined `$PYTHONPATH` - found corrupted paths
3. Attempted `unset PYTHONPATH` - temporary fix only
4. Tried `exec bash --noprofile --norc` - created clean shell
5. Ultimately decided to start fresh

**Key Learning:** Codespace environments can become corrupted during extensive debugging. A clean restart is often faster than continued troubleshooting.

### Phase 3: Fresh Start - Working Implementation

After recognizing the environment was too corrupted to reliably fix, a decision was made to create a completely fresh project with a clean, flat structure.

**New Structure Created:**

fresh_taskmanager/
├── manage.py
├── requirements.txt
├── myproject/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── api/
├── models.py
├── views.py
├── serializers.py
└── urls.py


**Why This Worked:**

| Decision | Rationale |
|----------|-----------|
| Flat directory structure | No nested folders to cause import issues |
| Clear project name (`myproject`) | Avoids confusion with `backend` naming |
| Simple app name (`api`) | No conflicts with Python modules |
| Minimal dependencies first | Added packages incrementally |
| SQLite for development | Zero configuration, reliable |

### Phase 4: Testing & Verification

The working API was tested using multiple methods:

1. **Django Browsable API** - Interactive testing in browser
2. **curl commands** - Command-line verification
3. **Postman** - Structured API testing (export included)

**Test Results:**

| Endpoint | Method | Status | Response Time |
|----------|--------|--------|---------------|
| `/api/register/` | POST | 201 Created | <200ms |
| `/api/login/` | POST | 200 OK | <150ms |
| `/api/tasks/` | GET | 200 OK | <100ms |
| `/api/tasks/` | POST | 201 Created | <150ms |
| `/api/tasks/{id}/` | GET | 200 OK | <100ms |
| `/api/tasks/{id}/` | PUT | 200 OK | <150ms |
| `/api/tasks/{id}/` | DELETE | 204 No Content | <100ms |

---

## Final Working Implementation

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Django | 4.2.0 |
| API Framework | Django REST Framework | 3.14.0 |
| Authentication | SimpleJWT | 5.3.0 |
| Database | SQLite3 | Built-in |
| Server | Gunicorn | 21.2.0 (production) |

### Project Structure

fresh_taskmanager/
├── manage.py # Django management script
├── requirements.txt # Python dependencies
├── runtime.txt # Python version for Render
├── db.sqlite3 # Development database
├── myproject/ # Project configuration
│ ├── init.py
│ ├── settings.py # Django settings
│ ├── urls.py # Main URL configuration
│ └── wsgi.py # WSGI entry point
└── api/ # Main application
├── init.py
├── models.py # Task data model
├── views.py # API view logic
├── serializers.py # Data serialization
├── urls.py # API endpoints
└── admin.py # Admin interface


### API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register/` | Create new user account | No |
| POST | `/api/login/` | Login and get JWT tokens | No |
| POST | `/api/refresh/` | Refresh expired access token | Refresh Token |
| GET | `/api/me/` | Get current user profile | Yes |
| GET | `/api/tasks/` | List all tasks for user | Yes |
| POST | `/api/tasks/` | Create a new task | Yes |
| GET | `/api/tasks/{id}/` | Get specific task | Yes |
| PUT/PATCH | `/api/tasks/{id}/` | Update a task | Yes |
| DELETE | `/api/tasks/{id}/` | Delete a task | Yes |

### Key Code: Task Model

```python
# api/models.py
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    Live Deployment

API URL: https://humble-broccoli-7g94jxrpxvv2x7pv-8000.app.github.dev/

## Lessons Learned

The most significant lesson from this development process is that **project structure matters enormously** in Django. The initial nested `backend/backend/` folder structure caused persistent import errors that wasted hours of debugging time. When environment corruption occurred (evidenced by `(venv)` appearing in the terminal while packages remained inaccessible), the most efficient solution was to abandon the corrupted environment and start fresh rather than continue fighting incremental issues. This experience reinforced the value of testing incrementally—registering a user, then logging in, then creating a task—rather than building all features before verifying any work. Additionally, committing working code to version control at each stable state proved invaluable, as it allowed for easy rollbacks when experiments failed. Finally, documenting every error message and attempted fix created a reference that prevented repeating the same mistakes in the final implementation. A clean, flat project structure with minimal dependencies and incremental testing is now my standard approach for any Django project.

Known Issues & Future Improvements

Current Limitations

SQLite database (not suitable for high-scale production)
No password reset functionality
No email notifications
Basic task model (no due dates, priorities, or tags)
Future Enhancements

PostgreSQL for production
Task filtering and search
Task priorities and due dates
Frontend React application

AI Usage Acknowledgement

AI tools were used for:

Some of the initial code structure generation
Debugging assistance (import errors, configuration)
Documentation formatting and review
All code has been reviewed, tested, and understood by the me. The debugging journey and final implementation represent original problem-solving work.


Submission Information

Backend Repository: https://github.com/bluTru3/backend_taskmanager
Working Code Location: /fresh_taskmanager/
Live API: https://tackmaster-api.onrender.com
Frontend Repository: https://github.com/bluTru3/task_manager_client

Conclusion

Despite significant technical challenges including nested folder structure issues, environment corruption, and import errors, a fully functional Task Management API was successfully implemented. The final solution demonstrates proper REST API design, JWT authentication, user-specific data isolation, and deployment readiness.

The working implementation is located in the /fresh_taskmanager directory of this repository.

