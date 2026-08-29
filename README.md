# Fitness Spark — Backend API

> Screenshots placeholder: _add product/UI screenshots here._

REST API powering **Fitness Spark**, a meal-planning application that helps users create personalized meal plans, discover healthy recipes, and track their nutrition goals. This repository contains the backend service only — the web frontend lives in the separate [`fitness-spark-frontend`](https://github.com/akalmannakarmi/fitness-spark-frontend) repository.

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.13+
- **Database:** MongoDB (via Motor async driver)
- **Authentication:** JWT (PyJWT, HS256) + bcrypt password hashing
- **Package manager:** uv
- **Quality tools:** ruff (lint + format), mypy (type checking), pre-commit
- **Tests:** pytest + pytest-asyncio
- **Infrastructure:** Docker / Docker Compose

## Prerequisites

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** (package manager)
- **MongoDB** (local install or via Docker Compose)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/akalmannakarmi/fitness-spark.git
cd fitness-spark
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

Set a value for `SECRET_KEY` — the application will **not** start without it. Generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Start MongoDB

Either run a local MongoDB instance, or use Docker Compose:

```bash
docker compose up -d mongodb
```

### 5. Run the server

```bash
uv run uvicorn app:app --reload
```

The API will be available at <http://localhost:8000>. Interactive API docs (Swagger UI) are at <http://localhost:8000/docs> and ReDoc at <http://localhost:8000/redoc>.

### 6. Seed data (optional)

The app ships with two standalone scripts for populating recipes:

- `fetchdata.py` — pulls recipe data from the Spoonacular API into local JSON files
- `loader.py` — loads those JSON files into MongoDB

To create an admin user for the admin endpoints:

```bash
uv run python tools.py
```

## API Overview

All routes return JSON. Authentication routes issue a JWT that must be sent on protected routes either as an `Authorization: Bearer <token>` header or a `token` query parameter. Admin routes require a token whose user has the `admin` group.

### Public Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Welcome message |
| POST | `/auth/signup` | Create a user account, returns JWT |
| POST | `/auth/login` | Authenticate and return a JWT |
| GET | `/api/v1/meal_plan/get/meal_plans` | List public meal plans |

### Authenticated User Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/auth/users/me` | Get the current user's profile |
| GET | `/api/v1/recipe/list/recipes` | List recipes (id + title) |
| GET | `/api/v1/recipe/get/recipes` | Paginated, filterable recipe list |
| GET | `/api/v1/recipe/get/recipe/{id}` | Get a single recipe |
| GET | `/api/v1/meal_plan/get/my/meal_plans` | List the current user's meal plans |
| GET | `/api/v1/meal_plan/get/meal_plan/{id}` | Get one of the user's meal plans |
| POST | `/api/v1/meal_plan/create/meal_plan` | Create a meal plan |
| PATCH | `/api/v1/meal_plan/update/meal_plan/{id}` | Update one of the user's meal plans |
| DELETE | `/api/v1/meal_plan/delete/meal_plan/{id}` | Delete one of the user's meal plans |

### Admin Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/admin/create/user` | Create a user with custom groups |
| GET | `/auth/admin/list/users/` | List all users (short form) |
| GET | `/auth/admin/get/users/` | Paginated, searchable user list |
| GET | `/auth/admin/get/user/{id}` | Get a single user |
| PUT | `/auth/admin/update/user/{id}` | Update a user |
| DELETE | `/auth/admin/delete/user/{id}` | Delete a user |
| GET | `/api/v1/admin/get/recipes` | Paginated, filterable recipe list (all) |
| GET | `/api/v1/admin/get/recipe/{id}` | Get any recipe |
| POST | `/api/v1/admin/create/recipe` | Create a recipe |
| PATCH | `/api/v1/admin/update/recipe/{id}` | Update a recipe |
| DELETE | `/api/v1/admin/delete/recipe/{id}` | Delete a recipe |
| GET | `/api/v1/admin/get/meal_plans` | List all meal plans |
| GET | `/api/v1/admin/get/meal_plan/{id}` | Get any meal plan |
| POST | `/api/v1/admin/create/meal_plan` | Create a meal plan |
| PATCH | `/api/v1/admin/update/meal_plan/{id}` | Update any meal plan |
| DELETE | `/api/v1/admin/delete/meal_plan/{id}` | Delete any meal plan |
| GET | `/stats/models` | List tracked models with document counts |
| GET | `/stats/model/{model_id}` | Get per-model request statistics |

### Recipe Filters

Recipe listing endpoints accept the following query parameters:

- `search` — free-text search
- `vegetarian`, `vegan`, `glutenFree`, `dairyFree`, `cheep` — boolean dietary filters
- `min_readyInMinutes`, `max_readyInMinutes` — time bounds
- `include_ingredients`, `exclude_ingredients` — ingredient lists
- `nutrients` — nutrient constraints (`{name: {min?: number, max?: number}}`)
- `page`, `limit` — pagination (default page 1, limit 10)

### Meal Plan Filters

Meal-plan listing endpoints accept: `search`, `recipe_ids` (list), `page`, `limit`.

## Running Tests

```bash
uv run pytest
```

Tests live under `auth/test/`. They require a running MongoDB (see `MONGO_URL` in `.env`).

## Docker

Build and run the full stack (MongoDB + API) with Docker Compose:

```bash
docker compose up --build
```

The API is exposed on port `8000`, MongoDB on port `27017`. Compose reads environment variables from `.env`.

To build and run the API image on its own:

```bash
docker build -t fitness-spark .
docker run --rm -p 8000:8000 --env-file .env fitness-spark
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding standards, and the pull request process.
