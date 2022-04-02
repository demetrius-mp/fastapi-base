# fastapi-base

FastAPI starter template using SQLModel. Includes JWT authentication and basic alembic configuration for migrations.

## Explaining the architecture

```
app
├── core
│   ├── dependencies.py
│   └── security.py
├── database.py
├── __init__.py
├── models
│   ├── __init__.py
│   └── user.py
├── routers
│   ├── auth.py
│   ├── http_exceptions.py
│   └── __init__.py
├── scripts.py
└── settings.py
```

`app/core/dependencies.py`: dependency injection code (database session, current user) should be here.

`app/core/security.py`: authentication code (hashing passwords, creating JWT's, adding a user to the database) should be here.
