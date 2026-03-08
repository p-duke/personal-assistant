# AGENTS.md

## Project Overview
Django 5.2 personal assistant application with task management and chat functionality.
The codebase follows clean architecture principles: **views → services → models**.
Uses PostgreSQL, PostgreSQL-specific features, and Python 3.11+ typing syntax.

---

## Build/Run Commands
```bash
python manage.py runserver              # Start development server
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create new migrations
python manage.py test                   # Run all tests
python manage.py test chat.tests        # Run single test file (chat/tests.py)
python manage.py test task_manager.tests # Run single test file (task_manager/tests.py)
python manage.py test chat.tests.<class>  #Run single test class
python manage.py test chat.tests.<method> #Run single test method (e.g., test_create_task)
python manage.py loaddata <fixture>     # Load database fixtures
python manage.py createsuperuser        # Create admin user
```

**Recommended workflow:**
1. Make changes to code
2. Run `python manage.py test` before committing
3. Use linting/typecheck commands if configured (e.g., `ruff check .` or `mypy .`)
4. Ensure pre-commit hooks pass if applicable

---

## Code Style Guidelines

### Python 3.11+ Syntax Preferences
- Use **union syntax**: `list | None`, `str | int`, `int | None`
- Import `from __future__ import annotations` at top of new files
- Use **keyword-only arguments** with `*` in service layer functions:
  ```python
  def create_task(*, title: str, priority: str = Task.NORMAL) -> Task:
      return Task.objects.create(title=title, priority=priority)
  ```
- Use `from __future__ import annotations` to enable delayed evaluation of type hints

### Import Ordering
1. **Django/stdlib imports** (sorted alphabetically)
2. **Third-party imports** (sorted alphabetically)
3. **Local project imports** (sorted, separated from above with blank line)

Example:
```python
from django.db import models
from django.utils import timezone

import requests

from .models import User
```

### Naming Conventions
| Type | Pattern | Examples |
|------|---------|----------|
| **Classes** | `PascalCase` | `Task`, `ChatMessage`, `MyViewSet` |
| **Functions** | `snake_case` | `get_user_tasks()`, `create_message()` |
| **Variables** | `snake_case` | `user_list`, `task_count` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_TASKS_PER_DAY = 10` |
| **Model fields** | `snake_case` | `title = models.CharField()`, `due_date = models.DateField()` |
| **Private members** | `_leading_underscore` | `def _private_helper():`, `self._cache` |

### Models & Services Patterns
- Always use Django's `timezone.now()` instead of `datetime.now()`
- Use Django's `TextChoices` for model fields (inherit from models.Model):
  ```python
  class Task(models.Model):
      class Priority(TextChoices):
          LOW = "low", "Low"
          NORMAL = "normal", "Normal"
          HIGH = "high", "High"
      status = models.CharField(max_length=10, choices=Status.choices)
  ```
- Use `update_fields` parameter in `.save()` for partial updates:
  ```python
  task.status = Task.Status.COMPLETE
  task.completed_at = timezone.now()
  task.save(update_fields=['status', 'completed_at', 'updated_at'])
  ```

---

## Error Handling & HTTP Status Codes

| Situation | Response Code | Notes |
|-----------|---------------|-------|
| Validation errors | **HTTP 400** | Invalid input data (DRF serializers should call `is_valid(raise_exception=True)`) |
| Object not found | **HTTP 404** | Resource does not exist |
| Permission denied | **HTTP 403** | User lacks permission to access resource |
| Server error | **HTTP 500** | Unexpected internal errors (should be rare with proper service layer) |

**DRF pattern:**
```python
# In DRF views
serializer.is_valid(raise_exception=True)
result = serializer.save()
```

---

## Testing Guidelines
- Write tests in `tests.py` files within app directories (e.g., `chat/tests.py`, `task_manager/tests.py`)
- **Test class inheritance:** All test classes inherit from `django.test.TestCase`
- **Descriptive naming:** `test_<scenario>_<expected_result>`
  - Example: `test_create_task_sets_status_to_open` or `test_daily_review_sums_overdue_tasks`
- **Assertion methods:** Use Django's assertion methods:
  - `assertEqual(a, b)`, `assertQuerySetEqual(queryset1, queryset2)`
  - `assertIsNone(obj)`, `assertTrue(condition)`, `assertFalse(condition)`
- **Override settings:** Use `@override_settings()` for test configuration changes
- **Integration tests:** Test views/services together (e.g., verify service returns correct queryset)
- **Unit tests:** Isolated pure functions without database access

---

## Django-Specific Architecture Patterns

**Layered Architecture:**
```
VIEW/DRF ViewSet → SERVICE layer → MODEL/Django ORM
      ↑              ↓  (orchestrates)    ↓
      └━━━━━━━━━━━━━━ business logic ━━━━┘
```

**Service layer responsibilities:**
- Business logic implementation
- Database queries and filtering
- Data transformation between models and serializers

**DRF View/ViewSet patterns:**
- Use `ModelViewSet` for standard CRUD operations
- Use `@action` decorator for custom endpoints with specific URLs:
  ```python
  @action(detail=True, methods=['post'])
  def complete(self, request, pk=None):
      task = self.get_object()
      return Response(TaskService.complete_task(task))
  ```
- Query filters via URL params: `/api/tasks/?status=open&overdue=true`

---

## Formatting Rules

| Rule | Value |
|------|-------|
| Indentation | **4-space** consistent spacing |
| Line length | **Max 100 characters** (prefer readability) |
| String quotes | Single quotes `'` unless escaped quotes needed |
| Trailing commas | Use in multi-line sequences and imports |
| Wildcard imports | **FORBIDDEN:** `from module import *` never use |

---

## Environment Configuration
- Load `.env` file using: `load_dotenv()` from python-dotenv
- Read config with defaults via `os.environ.get('VAR_NAME', default)`
- For optional configs: use `getenv('VAR', fallback_value)`
- **NEVER commit** secrets or `.env` files (add to gitignore)
- PostgreSQL database configuration via environment variables:
  - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
  - `POSTGRES_HOST`, `POSTGRES_PORT`

---

## AI Integration
The project includes Ollama support for local LLM integration (package: `ollama==0.1.6`). Use this library when interfacing with LLM endpoints.

---

## Third-Party Dependencies Summary
| Library | Version | Purpose |
|---------|---------|----------|
| Django | 5.2 | Core web framework |
| django-rest-framework | 3.16.1 | API views and serializers |
| psycopg2-binary | 2.9.11 | PostgreSQL adapter |
| python-dotenv | 1.2.1 | Environment variable loading |
| ollama | 0.1.6 | Local LLM integration |

