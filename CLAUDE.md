# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 5.2 personal assistant with task management and an LLM-powered chat interface. The chat layer parses natural language into structured intents and routes them to task management services. Uses Ollama for local LLM inference (no cloud dependency).

## Commands

```bash
python manage.py runserver              # Start dev server (localhost:8000)
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create new migrations
python manage.py test                   # Run all tests
python manage.py test chat.tests.ClassName.test_method  # Run a single test
ruff check .                            # Lint (E, F, I rules, max 100 chars)
```

## Architecture

The codebase enforces a strict layered pattern: **Views → Services → Models**. Views contain no business logic; all orchestration happens in `*/services.py`.

### Apps

**`task_manager/`** — Core task CRUD. Exposes both Django template views and a DRF `TaskViewSet` with custom `complete` and `daily_review` actions. Service functions use keyword-only args (`def create_task(*, title, priority, ...)`).

**`chat/`** — LLM chat interface. A user message flows through:
1. `parse_message()` — loads a prompt template from `chat/prompts/`, calls Ollama, validates JSON response against a Pydantic schema (`ChatResponseSchema`)
2. `handle_intent()` — routes the parsed intent to the appropriate `task_manager` service function
3. Response rendered via template or JSON API

Both apps expose two URL namespaces each:
- Template views: mounted at `/` (task_manager) and `/chat/`
- REST API: mounted at `/api/tasks/` and `/api/chat/`

### Adding a New Intent

1. Update `chat/prompts/detect_intent_extract_data.txt` with the new intent name
2. Add a Pydantic schema to `chat/schemas.py` if new fields are needed
3. Add a branch in `handle_intent()` in `chat/services.py`
4. Add the corresponding service function to `task_manager/services.py`

## Code Conventions

See `AGENTS.md` for full details. Key points:

- Use `from __future__ import annotations` and Python 3.11+ union syntax (`str | None`)
- Use `timezone.now()`, not `datetime.now()`
- Use `TextChoices` for model field enumerations
- Use `update_fields` in `.save()` for partial updates
- Single quotes, 4-space indent, 100-char line limit
- Test class naming: `test_<scenario>_<expected_result>`

## Environment

Requires a `.env` file with `POSTGRES_*` vars, `SECRET_KEY`, `DEBUG`, `OLLAMA_MODEL`, and `OLLAMA_HOST`. Ollama must be running locally (default: `http://localhost:11434`) with the configured model pulled.
