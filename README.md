# 🍕 **1337 Pizza** - Pizza Delivery for Your _Nerdy_ Needs

> _A Software Engineering University Course Project_

**1337 Pizza** is a pizza delivery company that has specialized in the needs of nerds.

## 📋 Project Overview

This repository contains all development artifacts related to the **backend service** of the 1337 Pizza delivery system. It exposes RESTful API endpoints that can be consumed by front-end applications. Front-end applications are out of scope for this repository and may be developed by other teams.

### Tech Stack

| Category              | Technology                                     |
| --------------------- | ---------------------------------------------- |
| **Framework**         | [FastAPI](https://fastapi.tiangolo.com/)       |
| **ORM**               | [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) |
| **Database**          | PostgreSQL 15                                  |
| **Migrations**        | [Alembic](https://alembic.sqlalchemy.org/)     |
| **Containerization**  | Docker & Docker Compose                        |
| **Orchestration**     | Kubernetes                                     |
| **Package Manager**   | Poetry                                         |
| **API Documentation** | Swagger UI (auto-generated)                    |

## 🏗️ Architecture & API Endpoints

The API follows a versioned structure (`/v1/...`) with the following resources:

| Endpoint          | Description        |
| ----------------- | ------------------ |
| `/v1/users`       | User management    |
| `/v1/order`       | Order processing   |
| `/v1/pizza-types` | Pizza type catalog |
| `/v1/toppings`    | Topping inventory  |
| `/v1/doughs`      | Dough options      |
| `/v1/sauces`      | Sauce selection    |
| `/v1/beverages`   | Beverage catalog   |

Full interactive API documentation is available at `http://localhost:8000/docs` when running locally.

## 🚀 Run the Application

**Quick Start**

**1. Clone the repository and start the containers:**

```bash
docker compose up --build
```

**2. Open a terminal in the web container and run database migrations:**

```bash
cd /web
PYTHONPATH=. alembic upgrade head
```

**3. Access the application:**

- **API Backend**: http://localhost:8000
- **Swagger UI Documentation**: http://localhost:8000/docs

## 🔄 CI/CD Pipeline Strategy

![CI/CD Pipeline Overview](doc/cicd_strategy/BPSE-CICD-Pipeline.png)

### Pipeline Stages

| Stage          | Trigger               | Environment                 | Tests & Jobs                                            |
| -------------- | --------------------- | --------------------------- | ------------------------------------------------------- |
| **Commit**     | All branches          | _Ephemeral_ (Dev Container) | Flake8 Linting, Integration Tests, SonarQube Analysis   |
| **Acceptance** | Merge Requests & Main | **Staging**                 | Deploy Staging, DB Migration, Smoke Test, Service Tests |
| **Release**    | Main branch only      | **Production**              | Deploy Production, DB Migration, Smoke Test             |

### Build Artifacts

| Artifact              | Purpose                                | Dockerfile                                                               |
| --------------------- | -------------------------------------- | ------------------------------------------------------------------------ |
| **Development Image** | Local dev & Commit stage testing       | [`development.dockerfile`](infra/build_artifacts/development.dockerfile) |
| **Release Image**     | Production-hardened, minimal footprint | [`release.dockerfile`](infra/build_artifacts/release.dockerfile)         |

📖 **Detailed documentation:** [CI/CD Strategy](doc/cicd_strategy/README.md)

## 🧪 Testing Strategy

This project employs a **multi-layered testing approach** to ensure quality at different levels:

### Test Types

| Type                  | Framework                                | Location             | Purpose                                    |
| --------------------- | ---------------------------------------- | -------------------- | ------------------------------------------ |
| **Unit Tests**        | pytest                                   | `tests/unit/`        | Schema validation, isolated business logic |
| **Integration Tests** | pytest                                   | `tests/integration/` | Database operations, CRUD functionality    |
| **Service Tests**     | [Tavern](https://tavern.readthedocs.io/) | `tests/service/`     | Full API endpoint testing (YAML-based)     |

### Running Tests

**Unit Tests:**

```bash
cd /web
PYTHONPATH=. pytest -x --junitxml=report_unit_tests.xml tests/unit/
```

**Integration Tests:**

```bash
cd /web
PYTHONPATH=. pytest -x tests/integration/
```

**Service Tests (Tavern):**

```bash
cd /web
export API_SERVER=localhost
export API_PORT=8000
PYTHONPATH=. pytest -x --junitxml=report_service_tests.xml --cov=app tests/service/
```

**Linting (Flakeheaven):**

```bash
cd /web
flakeheaven lint app/ tests/
```

📖 **Detailed documentation:** [Testing](doc/testing/README.md)

## 📁 Project Structure

```
1337-pizza/
├── app/                          # Application source code
│   ├── main.py                   # FastAPI application entry point
│   ├── api/v1/                   # API version 1
│   │   ├── router.py             # Main API router
│   │   └── endpoints/            # Resource endpoints (CRUD + schemas)
│   │       ├── beverage/
│   │       ├── dough/
│   │       ├── order/
│   │       ├── pizza_type/
│   │       ├── sauce/
│   │       ├── topping/
│   │       └── user/
│   ├── database/                 # Database layer
│   │   ├── connection.py         # DB connection handling
│   │   ├── models.py             # SQLAlchemy models
│   │   └── migrations/           # Alembic migrations
│   └── exceptions/               # Custom exceptions
├── tests/                        # Test suites
│   ├── unit/                     # Unit tests (pytest)
│   ├── integration/              # Integration tests (pytest)
│   └── service/                  # Service/API tests (Tavern)
├── doc/                          # Documentation
├── infra/                        # Infrastructure artifacts
│   ├── build_artifacts/          # Dockerfiles & scripts
│   └── deployment/               # Kubernetes manifests
├── docker-compose.yml            # Local development setup
├── pyproject.toml                # Poetry dependencies & config
├── alembic.ini                   # Alembic configuration
└── mypy.ini                      # Type checking configuration
```

## 📚 Documentation

| Document                                                            | Description                        |
| ------------------------------------------------------------------- | ---------------------------------- |
| 📖 [Documentation Overview](doc/README.md)                          | Entry point for all documentation  |
| 🛠️ [Local Development Setup](doc/local_dev_setup/README.md)         | IDE setup guide (PyCharm)          |
| 🏛️ [Domain Model](doc/domain_model/README.md)                       | Entity definitions & relationships |
| 🔄 [CI/CD Strategy](doc/cicd_strategy/README.md)                    | Pipeline architecture & stages     |
| 🧪 [Testing](doc/testing/README.md)                                 | Test execution guide               |
| 📝 [Coding Conventions](doc/coding_conventions/README.md)           | PEP 8 style guide & naming         |
| 🔧 [Tooling](doc/tooling/README.md)                                 | Tools & frameworks overview        |
| 📋 [Versioning & Commits](doc/versioning_commit_messages/README.md) | Git workflow & conventions         |

## ⚠️ Notice

> **This repository is mirrored from the university's GitLab, so it only contains the code and does not include the issues, milestones, pipeline, or other features.**
