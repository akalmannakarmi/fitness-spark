# Fitness Spark — Backend API

> Screenshots placeholder: _add product/UI screenshots here._

REST API powering **Fitness Spark**, a meal-planning application that helps users create personalized meal plans, discover healthy recipes, and track their nutrition goals. This repository contains the backend service only — the web frontend lives in the separate [`fitness-spark-frontend`](https://github.com/akalmannakarmi/fitness-spark-frontend) repository.

## Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.13+
- **Database:** MongoDB (via pymongo `AsyncMongoClient`)
- **Authentication:** JWT (PyJWT, HS256) + bcrypt password hashing
- **Package manager:** uv
- **Quality tools:** ruff (lint + format), mypy (type checking), pre-commit
- **Tests:** pytest + pytest-asyncio (httpx ASGI transport, no live server)
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

The app ships with standalone scripts under `scripts/` for populating recipes and users:

- `fetch_recipes.py` — pulls recipe data from the Spoonacular API into `recipies_*.json` dumps
- `load_recipes.py` — loads those JSON dumps into MongoDB
- `create_admin.py` — interactive CLI that creates an admin user
- `migrate_rename_cheep.py` — one-off migration renaming the legacy `cheep` field to `cheap`

The fetch and load scripts use `requests`, which lives in the optional `tools` extra. Install it once and run the scripts from the repo root:

```bash
uv sync --extra tools
uv run python scripts/fetch_recipes.py --api-key YOUR_KEY --cuisine Thai
uv run python scripts/load_recipes.py
uv run python scripts/create_admin.py
```

`fetch_recipes.py` accepts `--api-key` (or the `SPOONACULAR_API_KEY` env var), `--cuisine`, `--number` (recipes per request), and `--offset`.

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

## Project Structure

The backend is organized by domain:

```
app.py            # FastAPI instance + router wiring (uvicorn target: app:app)
main.py           # dev entry point (env-driven reload)
config.py         # pydantic-settings Settings (single source of env)
database.py       # ONE AsyncMongoClient + collections
security.py       # password hashing + JWT helpers
exceptions.py     # CustomAPIException + handlers
deps.py           # get_current_user, require_admin
schemas/          # pydantic request/response models (common, user, recipe, meal_plan, stats)
crud/             # data-access functions (users, recipes, meal_plans, stats)
api/              # routers (auth, admin_users, recipes, meal_plans, admin, stats)
scripts/          # standalone CLI tools (create_admin, fetch_recipes, load_recipes, migrate_rename_cheep)
tests/            # pytest suite (httpx ASGI transport)
```

## Running Tests

Tests live under `tests/` and use httpx's ASGI transport against the app in-process — **no live server required**. They do need a running MongoDB (see `MONGO_URL` in `.env`); tests use a dedicated `fitness_spark_test` database that is cleaned up after each test.

```bash
docker compose up -d mongodb
uv run pytest
```

To run a single test file or by name:

```bash
uv run pytest tests/test_auth.py
uv run pytest -k "login"
```

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
