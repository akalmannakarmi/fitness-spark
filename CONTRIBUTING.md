# Contributing

Thanks for taking the time to contribute to **Fitness Spark**! These guidelines apply to this backend repository and are also referenced by the frontend repository.

## Table of Contents

- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Pre-Commit Hooks](#pre-commit-hooks)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Branching Strategy](#branching-strategy)

## Development Environment

1. Clone the repository and install dependencies with [uv](https://docs.astral.sh/uv/):

   ```bash
   git clone https://github.com/akalmannakarmi/fitness-spark.git
   cd fitness-spark
   uv sync
   ```

2. Create a `.env` from the example and set `SECRET_KEY`:

   ```bash
   cp .env.example .env
   ```

3. Start MongoDB (or use `docker compose up -d mongodb`).

4. Run the API:

   ```bash
   uv run uvicorn app:app --reload
   ```

5. Run the test suite:

   ```bash
   uv run pytest
   ```

For the frontend repo, use `bun install` and `bun run dev` instead.

## Coding Standards

Standards are enforced by configured tools which run in CI. Keep them passing locally before pushing:

- **Formatting:** [ruff format](https://docs.astral.sh/ruff/formatter/) — line length 88, double quotes, spaces.
  ```bash
  uv run ruff format .
  uv run ruff format --check .
  ```
- **Linting:** [ruff check](https://docs.astral.sh/ruff/linter/) with rulesets `E, F, I, N, UP, B, A, C4, SIM, TCH`.
  ```bash
  uv run ruff check .
  ```
- **Type checking:** [mypy](https://mypy-lang.org/) in strict mode.
  ```bash
  uv run mypy .
  ```
- **Python:** `requires-python = ">=3.13"`. Use type hints on all new code and run mypy cleanly rather than sprinkling `# type: ignore` (add a targeted ignore only where a third-party type boundary genuinely blocks strict checking).

Configuration lives in `pyproject.toml`.

## Pre-Commit Hooks

This repository uses [pre-commit](https://pre-commit.com/) to automatically run ruff (lint + format), mypy, and a few safety checks before each commit.

Install the hooks once after `uv sync`:

```bash
uv run pre-commit install
```

Hooks run every commit. To run them manually against all files:

```bash
uv run pre-commit run --all-files
```

If a hook reformats or fixes a file, review the changes, stage them, and commit again.

## Commit Message Conventions

Use concise [Conventional Commits](https://www.conventionalcommits.org/) style messages:

```
<type>(<scope>): <short summary>
```

- **types:** `feat`, `fix`, `build`, `chore`, `ci`, `docs`, `refactor`, `style`, `test`, `perf`
- **scope:** optional, e.g. `auth`, `recipe`, `meal-plan`, `docker`, `ci`
- **summary:** imperative mood, lowercase, no trailing period, ≤ ~72 characters

Examples:

```
feat(auth): add refresh token rotation
fix(recipe): guard against empty ingredient list
docs: update API reference in README
```

## Pull Request Process

1. Create a feature branch off `main` (see [Branching Strategy](#branching-strategy)).
2. Make your changes, keeping the diff small and focused. If a change spans both repos, raise a PR for each.
3. Ensure all quality gates pass locally:
   - `uv run ruff format --check .`
   - `uv run ruff check .`
   - `uv run mypy .`
   - `uv run pytest`
4. Push the branch and open a pull request targeting `main`.
5. Fill in the PR description: what changed, why, and how to test it (screenshots for UI changes).
6. Continuous integration will run the same lint, format, type-check, and test gates. A PR must pass CI before it is merged.
7. Request a review; address review feedback; keep the conversation focused.

## Branching Strategy

- `main` is the protected, always-deployable branch.
- Development happens on feature branches (`revamp/**` for the ongoing modernization, or descriptive names like `feat/meal-plan-multi-user`).
- Prefer splitting large changes into smaller, reviewable PRs.

Thank you for contributing!
