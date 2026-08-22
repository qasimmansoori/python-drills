# 💼 Job Application Tracker API (Modular Architecture)

A production-grade, modular REST API built with **FastAPI**, **Pydantic v2**, and **Python 3.12** for managing and tracking software engineering job applications.

---

## 🏛️ Architecture & Directory Structure

```text
projects/job_tracker/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── applications.py   # Application CRUD routes
│   │       └── router.py             # API v1 Router aggregator
│   ├── core/
│   │   ├── exceptions.py             # Custom domain exceptions & handlers
│   │   └── middleware.py             # Request timing middleware (X-Process-Time)
│   ├── schemas/
│   │   └── application.py            # Pydantic validation schemas
│   └── main.py                       # FastAPI application factory
└── README.md
```

---

## 🚀 Running the API Locally

```bash
uv run uvicorn projects.job_tracker.app.main:app --reload
```

- **Interactive API Docs (Swagger UI):** `http://127.0.0.1:8000/docs`
- **Alternative ReDoc UI:** `http://127.0.0.1:8000/redoc`
- **Health Check:** `http://127.0.0.1:8000/health`

---

## 🛡️ Key Backend Features
- **Strict Schema Isolation:** `JobApplicationCreate` and `JobApplicationResponse` models.
- **Dependency Injection:** Modular query pagination and admin header verification.
- **Global Exception Interception:** Standardized JSON error envelope on 404 / 409 conflicts.
- **Execution Timing Middleware:** Injects `X-Process-Time` onto every HTTP response.
