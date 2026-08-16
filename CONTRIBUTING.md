# Contributing to Reddit MCP Server

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Development Setup

1. **Fork the repository** and clone your fork locally.
2. **Install Python 3.11+**.
3. **Install dependencies** including development tools:
   ```bash
   pip install -e ".[dev]"
   ```
4. **Familiarize yourself with the architecture**: Read `docs/architecture.md`.

## Workflow

1. Create a branch for your feature or bug fix: `git checkout -b feature/my-new-feature`
2. Make your changes.
3. Ensure your code passes linting and formatting:
   ```bash
   ruff check .
   ruff format .
   ```
4. Run the tests to ensure you haven't broken anything:
   ```bash
   pytest tests/
   ```
5. Commit your changes: `git commit -am 'Add some feature'`
6. Push to the branch: `git push origin feature/my-new-feature`
7. Submit a pull request.

## Pull Request Process

1. Ensure your PR description clearly describes the problem and solution.
2. If your PR changes behavior, ensure you have updated the tests.
3. Your PR will be automatically tested and linted by GitHub Actions. Ensure all checks pass.
4. A maintainer will review your PR and may request changes.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. See `CODE_OF_CONDUCT.md`.
