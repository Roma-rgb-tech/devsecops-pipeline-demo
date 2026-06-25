# Contributing to DevSecOps Pipeline Demo

Thank you for your interest in contributing! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/devsecops-pipeline-demo.git
   cd devsecops-pipeline-demo
   ```
3. Install dependencies:
   ```bash
   make install
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Make your changes
3. Run tests and linting:
   ```bash
   make test
   make lint
   ```
4. Commit with a descriptive message (we follow [Conventional Commits](https://www.conventionalcommits.org/)):
   ```
   feat: add /metrics endpoint
   fix: handle 404 on missing item
   docs: update API reference
   chore: bump dependencies
   ```
5. Push and open a Pull Request

## Code Style

- **Python**: formatted with [black](https://black.readthedocs.io/), linted with [ruff](https://docs.astral.sh/ruff/)
- **Commits**: follow Conventional Commits spec
- **Tests**: every new endpoint or feature must have tests

## Running Tests

```bash
make test          # run full suite with coverage
pytest tests/ -v   # verbose output
```

## Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue template.

## Requesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) issue template.

## Security Issues

Please **do not** open public issues for security vulnerabilities. Email the maintainer directly or use GitHub's private security advisory feature.