# Contributing

Thanks for considering contributing!

## Quickstart

1) Fork the repo and create a feature branch.
2) Install dev dependencies:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

3) Install and enable git hooks:

```bash
pre-commit install
```

4) Run checks locally:

```bash
ruff format .
ruff check .
pytest
```

## Pull requests

- Keep PRs focused and small when possible.
- Include a short summary and screenshots for UI changes.
- Add or update tests when changing behavior.

## Code style

- Formatting and linting: `ruff` (see `pyproject.toml`).
- Tests: `pytest` + `pytest-django`.

