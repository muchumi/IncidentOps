# 🚨 IncidentOps

**IncidentOps** is a RESTful helpdesk and incident-management API built with **FastAPI** and **Python**.

The project provides a backend foundation for managing operational incidents and helpdesk requests through a modern, lightweight API architecture. It is designed to be extended with incident tracking, ticket management, authentication, database persistence, and automated incident workflows.

---

## 📌 Project Overview

IncidentOps provides an API service for handling incidents and operational support requests.

The application is built around **FastAPI**, making it suitable for:

- Helpdesk and support systems
- Incident tracking
- IT operations management
- Internal service-desk applications
- REST API integrations
- Future web or mobile frontends

The current application initializes the database automatically when the API starts and exposes a basic health/root endpoint.

---

## ✨ Features

### Current Features

- ⚡ FastAPI-based REST API
- 🐍 Python backend
- 🗄️ SQLite database
- 🔧 SQLAlchemy database integration
- 📦 Modular `api` package structure
- 🚀 Automatic database table creation on application startup
- 📖 Interactive API documentation through FastAPI
- 🔌 Extensible architecture for future incident and ticket-management features

### Planned / Extensible Features

The architecture can be extended to support:

- 🎫 Helpdesk ticket creation and management
- 🚨 Incident reporting
- 📊 Incident status tracking
- 👥 User and support-agent management
- 🔐 Authentication and authorization
- 🏷️ Ticket priorities and categories
- 💬 Ticket comments and communication
- 📎 File and evidence attachments
- 🔔 Notifications
- 📈 Incident analytics
- 📝 Incident history and audit trails
- 🔄 Incident lifecycle workflows

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Backend programming language |
| **FastAPI** | REST API framework |
| **SQLAlchemy** | Database ORM |
| **SQLite** | Development database |
| **Uvicorn** | ASGI application server |
| **Pydantic** | Data validation and API schemas |

---

## 📁 Project Structure

The repository currently follows a modular API-oriented structure:

```text
IncidentOps/
│
├── api/
│   ├── main.py
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   └── services/
│
├── incidentOps.db
│
└── README.md
```

> The exact contents of the `models`, `schemas`, `routers`, and `services` packages may evolve as the project develops.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/muchumi/IncidentOps.git
```

Navigate into the project:

```bash
cd IncidentOps
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Alternatively, install the core dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

---

# ▶️ Running the API

From the project root, start the application with:

```bash
uvicorn api.main:app --reload
```

On Windows, if `uvicorn` is not available directly, use:

```powershell
python -m uvicorn api.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

These interfaces allow developers to explore and test available API endpoints directly from their browser.

---

# 🔌 API

## Root Endpoint

### `GET /`

Returns a basic response confirming that the IncidentOps API is running.

### Example

```bash
curl http://127.0.0.1:8000/
```

### Response

```json
{
    "message": "Hello World!"
}
```

The current FastAPI application defines the root route with an HTTP `200 OK` response.

---

# 🗄️ Database

IncidentOps currently uses **SQLite** for database persistence.

The repository contains:

```text
incidentOps.db
```

Database configuration is handled through the API database module.

At application startup, SQLAlchemy is used to create the configured database tables:

```python
Base.metadata.create_all(bind=engine)
```

This makes SQLite convenient for local development and testing.

---

## 🔄 Future Database Improvements

For production deployments, the project can be extended to support databases such as:

- PostgreSQL
- MySQL
- MariaDB

A migration framework such as **Alembic** can also be introduced to manage database schema changes safely.

---

# 🧪 Testing

Tests should be placed in a dedicated test package, for example:

```text
api/
└── tests/
    ├── test_incidents.py
    ├── test_tickets.py
    ├── test_users.py
    └── conftest.py
```

Run the test suite with:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

---

# 🔐 Security Considerations

Before deploying IncidentOps to production, authentication and authorization should be implemented.

Recommended security improvements include:

- JWT or OAuth2 authentication
- Role-based access control
- Password hashing
- Input validation
- Rate limiting
- CORS configuration
- Secure HTTP deployment
- Environment-based configuration
- Database credential protection
- Audit logging
- Secrets management

**Never commit passwords, API keys, tokens, or other secrets to Git.**

Use environment variables instead:

```env
DATABASE_URL=sqlite:///./incidentOps.db
SECRET_KEY=your-secret-key
```

---

# 🌐 Production Deployment

For production, the application can be deployed behind a reverse proxy such as:

- Nginx
- Caddy
- Traefik

A typical production command is:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

For larger deployments, multiple application workers can be configured depending on the hosting environment.

---

# 🧩 Architecture

The intended architecture separates the application into different responsibilities:

```text
                    ┌─────────────────────┐
                    │      Client         │
                    │ Web / Mobile / API  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       Routes        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Services       │
                    │ Business Logic      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Models        │
                    │     SQLAlchemy      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       SQLite        │
                    │   incidentOps.db    │
                    └─────────────────────┘
```

This separation makes the application easier to test, maintain, and expand.

---

# 🛣️ Roadmap

The following features can be introduced as IncidentOps evolves:

### Phase 1 — Core API

- [x] FastAPI application
- [x] Database initialization
- [x] Root API endpoint
- [ ] Incident model
- [ ] Ticket model
- [ ] CRUD endpoints

### Phase 2 — Helpdesk

- [ ] Ticket creation
- [ ] Ticket assignment
- [ ] Ticket priority
- [ ] Ticket categories
- [ ] Ticket status management
- [ ] Ticket comments
- [ ] Ticket history

### Phase 3 — Incident Management

- [ ] Incident severity levels
- [ ] Incident lifecycle
- [ ] Incident assignment
- [ ] Incident timelines
- [ ] Root-cause tracking
- [ ] Resolution records
- [ ] Post-incident reviews

### Phase 4 — Security

- [ ] User authentication
- [ ] JWT authentication
- [ ] Role-based authorization
- [ ] Admin functionality
- [ ] Audit logging

### Phase 5 — Operations

- [ ] Notifications
- [ ] Email integration
- [ ] Webhooks
- [ ] Metrics
- [ ] Reporting dashboard
- [ ] Production database support

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git fork https://github.com/muchumi/IncidentOps.git
```

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 3. Make your changes

Follow the existing project structure and keep business logic separated from API routes where possible.

### 4. Run tests

```bash
pytest -v
```

### 5. Commit your changes

```bash
git add .
git commit -m "feat: add your feature"
```

### 6. Push your branch

```bash
git push origin feature/your-feature
```

### 7. Open a Pull Request

Describe:

- What was changed
- Why it was changed
- How it was tested
- Any additional configuration required

---

# 🐛 Reporting Issues

If you find a bug or have a feature request, open an issue in the GitHub repository.

Please include:

- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version
- Operating system
- Relevant error messages or logs

---

# 📄 License

A license should be added to the repository before distributing IncidentOps as an open-source project.

Recommended options include:

- MIT License
- Apache License 2.0
- GNU GPLv3

Until a license is explicitly added to the repository, the project should not be assumed to be freely reusable under a particular open-source license.

---

# 👨‍💻 Author

**Muchumi**

GitHub:

https://github.com/muchumi

Project:

https://github.com/muchumi/IncidentOps

---

## ⭐ Project Status

**IncidentOps — FastAPI Helpdesk & Incident Management API**

The project is currently under active development. The existing repository provides the FastAPI foundation and database initialization, with additional helpdesk and incident-management functionality intended to be built on top of the current architecture.

---

### Built With ❤️ Using FastAPI

```text
Python + FastAPI + SQLAlchemy + SQLite
```