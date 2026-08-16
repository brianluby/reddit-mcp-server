# .github/ISSUE_TEMPLATE/bug_report.md

```md
---
name: "🐛 Bug Report"
about: Report a bug to help us improve the Reddit MCP Server
title: "[BUG] "
labels: bug
assignees: ""
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run the server using tool '...' with arguments '...'
2. See error in logs/client output

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Environment Details (please complete the following information):**
- OS: [e.g. macOS, Ubuntu, Windows]
- Python Version: [e.g. 3.11, 3.12]
- MCP Client: [e.g. Claude Desktop, Cursor, Zed]

**Additional Context**
Add any other context about the problem here (e.g., error logs from `sys.stderr`).
```

# .github/ISSUE_TEMPLATE/feature_request.md

```md
---
name: "🚀 Feature Request"
about: Suggest an idea or a new tool for this MCP server
title: "[FEATURE] "
labels: enhancement
assignees: ""
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. "I want to be able to search subreddits using specific filters..."

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional Context**
Add any other context or mockups about the feature request here.
```

# .github/pull_request_template.md

```md
### Description

Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context. 

Fixes # (issue)

### Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

### How Has This Been Tested?

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce.

- [ ] All unit tests pass locally (`pytest tests/`)
- [ ] Successfully tested with the MCP Inspector (`npx @modelcontextprotocol/inspector ...`)

### Checklist:

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

# .github/workflows/ci.yml

```yml
name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"
        cache: "pip"
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
        
    - name: Lint with ruff
      run: |
        ruff check .
        
    - name: Check formatting with ruff
      run: |
        ruff format --check .
        
    - name: Test with pytest
      run: |
        pytest tests/

```

# .github/workflows/release.yml

```yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write # Required for PyPI trusted publishing
      contents: read
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"
        
    - name: Install build tool
      run: python -m pip install --upgrade build
        
    - name: Build package
      run: python -m build
        
    - name: Publish package to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1

```

# .gitignore

```
# Environments
.env
.venv
env/
venv/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
dist/
build/
*.egg-info/

# Pytest / Coverage
.pytest_cache/
.coverage
coverage.xml

# IDEs
.vscode/
.idea/

```

# .pytest_cache/.gitignore

```
# Created by pytest automatically.
*

```

# .pytest_cache/CACHEDIR.TAG

```TAG
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html

```

# .pytest_cache/README.md

```md
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

```

# .pytest_cache/v/cache/lastfailed

```
{
  "tests/test_tools.py::test_extract_public_opinion_tool": true
}
```

# .pytest_cache/v/cache/nodeids

```
[
  "tests/test_auth.py::test_auth_manager_http_error",
  "tests/test_auth.py::test_auth_manager_missing_env",
  "tests/test_auth.py::test_auth_manager_success",
  "tests/test_http.py::test_http_client_429_max_retries",
  "tests/test_http.py::test_http_client_429_retry_success",
  "tests/test_http.py::test_http_client_success",
  "tests/test_reddit_client.py::test_get_post_thread_appends_json",
  "tests/test_reddit_client.py::test_get_post_thread_malformed_json",
  "tests/test_reddit_client.py::test_get_post_thread_success",
  "tests/test_reddit_client.py::test_get_subreddit_trends_error",
  "tests/test_reddit_client.py::test_get_subreddit_trends_rate_limit",
  "tests/test_reddit_client.py::test_get_subreddit_trends_success",
  "tests/test_tools.py::test_analyze_niche_trends",
  "tests/test_tools.py::test_analyze_niche_trends_tool",
  "tests/test_tools.py::test_explore_discussions_tool",
  "tests/test_tools.py::test_explore_reddit_discussions",
  "tests/test_tools.py::test_explore_reddit_discussions_pagination",
  "tests/test_tools.py::test_extract_post_threads",
  "tests/test_tools.py::test_extract_public_opinion",
  "tests/test_tools.py::test_extract_public_opinion_logic",
  "tests/test_tools.py::test_extract_public_opinion_tool",
  "tests/test_tools.py::test_get_subreddit_trends",
  "tests/test_tools.py::test_parse_comment_data",
  "tests/test_tools.py::test_parse_comment_data_more",
  "tests/test_tools.py::test_parse_post_data",
  "tests/test_tools.py::test_search_knowledge",
  "tests/test_tools.py::test_search_knowledge_empty_results",
  "tests/test_tools.py::test_search_knowledge_filters_short_titles",
  "tests/test_tools.py::test_search_knowledge_tool",
  "tests/test_tools.py::test_search_reddit",
  "tests/test_tools.py::test_tool_llm_timeout",
  "tests/test_tools.py::test_truncate_text_util"
]
```

# .ruff_cache/.gitignore

```
# Automatically created by ruff.
*

```

# .ruff_cache/0.16.3/16929662823713726873

This is a binary file of the type: Binary

# .ruff_cache/CACHEDIR.TAG

```TAG
Signature: 8a477f597d28d172789f06886806bc55
```

# CODE_OF_CONDUCT.md

```md
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.

```

# CONTRIBUTING.md

```md
# Contributing to Reddit MCP Server

First off, thanks for taking the time to contribute!

The following is a set of guidelines for contributing to this project. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Development Setup

1. **Fork the repository** and clone your fork locally.
2. **Install Python 3.11+**.
3. **Install dependencies** including development tools:
   \`\`\`bash
   pip install -e ".[dev]"
   \`\`\`
4. **Familiarize yourself with the architecture**: Read `docs/architecture.md`.

## Workflow

1. Create a branch for your feature or bug fix: `git checkout -b feature/my-new-feature`
2. Make your changes.
3. Ensure your code passes linting and formatting:
   \`\`\`bash
   ruff check .
   ruff format .
   \`\`\`
4. Run the tests to ensure you haven't broken anything:
   \`\`\`bash
   pytest tests/
   \`\`\`
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

```

# Dockerfile

```
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir build hatchling

# Copy the project files
COPY pyproject.toml README.md ./
COPY src/ src/

# Build the wheel
RUN python -m build --wheel

# Stage 2: Runtime environment
FROM python:3.11-slim

WORKDIR /app

# Copy the built wheel from the builder stage
COPY --from=builder /app/dist/*.whl ./

# Install the wheel
RUN pip install --no-cache-dir ./*.whl && rm ./*.whl

# The server communicates via standard I/O, so we don't expose ports.
# We set the entrypoint to the CLI command defined in pyproject.toml
ENTRYPOINT ["reddit-mcp"]

```

# docs/architecture.md

```md
# Reddit MCP Server Architecture

This project is built using a strict 4-Layer Architecture to separate concerns, ensure testability, and provide a professional codebase structure.

## Layer Overview

1. **Domain Layer (`domain/`)**: The core of the application. Contains the Pydantic models representing the business entities (e.g., `RedditPost`, `RedditComment`, `RedditThread`). This layer has no dependencies on other layers.
2. **Infrastructure Layer (`infrastructure/`)**: Handles communication with the outside world. This includes the asynchronous HTTP clients for Reddit (`RedditClient`) and DuckDuckGo (`DuckDuckGoSearchClient`), as well as logging setup.
3. **Application Layer (`application/`)**: Contains the business logic and the actual MCP tools (`tools.py`). It orchestrates data flow by calling the infrastructure clients and mapping the raw data to Domain models.
4. **Interface Layer (`interface/`)**: The entry point for the application. Contains the FastMCP server setup (`server.py`) which registers the application tools and exposes them via the Standard IO transport.

## Data Flow Diagram

\`\`\`mermaid
graph TD
    subgraph Interface Layer
        MCP[FastMCP Server]
    end

    subgraph Application Layer
        Tools[MCP Tools]
        Utils[Truncation Utilities]
    end

    subgraph Infrastructure Layer
        RedditClient[Reddit HTTP Client]
        DDGClient[DuckDuckGo Search Client]
    end

    subgraph Domain Layer
        Models[Pydantic Models]
    end

    MCP -->|Registers & Invokes| Tools
    Tools -->|Uses| Utils
    Tools -->|Fetches Data| RedditClient
    Tools -->|Searches URLs| DDGClient
    Tools -->|Returns| Models
    RedditClient -->|Raw JSON| Tools
    DDGClient -->|Raw URLs| Tools
\`\`\`

## Benefits of this Architecture
- **Testability**: We can easily mock the `Infrastructure Layer` to test the `Application Layer` without making real network requests.
- **Maintainability**: If Reddit changes its API, we only need to update the `Infrastructure Layer` and mapping functions, leaving the `Domain` and `Interface` untouched.
- **Scalability**: New tools or alternative data sources can be seamlessly integrated.

```

# pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "reddit-mcp-server"
version = "0.1.0"
description = "A production-grade, open-source Reddit MCP Server"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=0.4.1",
    "mcp>=1.0.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.0.0",
    "httpx>=0.27.0",
    "ddgs>=9.14.4",
]

[project.scripts]
reddit-mcp = "reddit_mcp.main:main"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.4.0",
    "build>=1.2.0"
]

[tool.hatch.build.targets.wheel]
packages = ["src/reddit_mcp"]

```

# README.md

```md
# 🤖 Reddit MCP Server (AI-Native Edition)

[![CI Status](https://github.com/ismailsaoulaj/reddit-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/ismailsaoulaj/reddit-mcp-server/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A highly resilient, open-source [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. It empowers AI models (such as Claude and Cursor) to search, fetch, read, and deep-dive into Reddit content with robust rate-limiting recovery and smart comment-filtering.

Built in Python using `FastMCP`, this project adheres to a strict **4-Layer Architecture** designed for high modularity, testability, and painless contributions.

---

## 🗺️ How it Works (Data Flow Sequence)

Here is a visual sequence diagram of how the AI model interacts with this server to retrieve Reddit insights:

\`\`\`mermaid
sequenceDiagram
    autonumber
    actor AI as AI Assistant (Claude/Cursor)
    participant MCP as FastMCP Server (STDIO)
    participant Tools as Application Tools
    participant Reddit as Reddit API (httpx)
    participant DDG as DuckDuckGo Provider

    AI->>MCP: Request (e.g., search_knowledge)
    MCP->>Tools: Route request
    alt Global Search (Default fallback)
        Tools->>DDG: Execute Query
        DDG-->>Tools: Return curated Reddit URLs
    end
    Tools->>Reddit: Fetch Thread (Resilient HTTP Client)
    Note over Reddit,Tools: Handles 429 (Rate Limits) with Retry-After backoff!
    Reddit-->>Tools: Return JSON payload
    Tools->>Tools: Refine comments (filter bots & short noise)
    Tools-->>MCP: Map to Domain Models (Pydantic)
    MCP-->>AI: Return clean JSON-RPC Response (stdout-safe)
\`\`\`

---

## ✨ Features

- 🛡️ **Fail-Fast Configuration:** Utilizes `pydantic-settings` to validate credentials at boot, preventing runtime failures.
- 📈 **Resilient HTTP Client:** Built-in exponential backoff and rate-limiting recovery. If Reddit says `429 Too Many Requests`, the server respects the `Retry-After` header and retries automatically.
- 🔍 **Strategic Search:** Integrates a decoupled search provider system (Strategy Pattern) allowing easy addition of Google/Tavily search engines.
- 🤖 **LLM-Safe Filtering:** Cleans thread payloads by dropping auto-moderators, bot notifications, and low-quality comments, saving precious LLM token costs.
- ⏱️ **Strict LLM Timeout Protection:** Uses decorators to force safe API timeouts, returning clean graceful JSON-RPC fallbacks instead of hanging.

---

## ⚙️ Prerequisites & Setup

### Requirements

- Python 3.11 or higher
- Reddit API App credentials (Client ID and Client Secret)

### Quick Start (Local Installation)

1. **Clone and Install:**

\`\`\`bash
git clone https://github.com/ismailsaoulaj/reddit-mcp-server.git
cd reddit-mcp-server
pip install -e .
\`\`\`

2. **Configure your environment:**

Create a `.env` file in the root directory:

\`\`\`env
REDDIT_CLIENT_ID="your_client_id_here"
REDDIT_CLIENT_SECRET="your_client_secret_here"
\`\`\`

---

## 🐳 Docker Installation

A multi-stage Dockerfile is provided for seamless execution.

\`\`\`bash
docker build -t reddit-mcp-server .
\`\`\`

> **Note:** If using Docker, replace the `command` in client configs with `docker` and arguments with `run -i --rm reddit-mcp-server`.

---

## 🛠️ Configuration for AI Clients

### 1. Claude Desktop

Edit your configuration file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

\`\`\`json
{
  "mcpServers": {
    "reddit": {
      "command": "hatch",
      "args": [
        "run",
        "reddit-mcp"
      ],
      "cwd": "/absolute/path/to/reddit-mcp-server"
    }
  }
}
\`\`\`

### 2. Cursor

Go to **Settings > Features > MCP** and add a new command-based server:
- **Type:** command
- **Name:** Reddit
- **Command:** `hatch run reddit-mcp` (using the absolute path to your python/hatch environment)

---

## 🧪 Developer Experience (DX) & Testing

We prioritize high test coverage. We mock all network traffic, ensuring tests run instantly and reliably.

### Run Tests

\`\`\`bash
# Install development dependencies
pip install -e ".[dev]"

# Execute pytest
pytest tests/
\`\`\`

### Manual Testing with the MCP Inspector

\`\`\`bash
npx @modelcontextprotocol/inspector hatch run reddit-mcp
\`\`\`

This will launch a web browser UI where you can invoke the `search_reddit`, `get_subreddit_trends`, and `extract_post_threads` tools directly and inspect the JSON responses.

---

## 🤝 Contributing & Architecture

We love contributions! Please check out `docs/architecture.md` for architectural details and view `src/reddit_mcp/infrastructure/search/providers/README.md` to learn how to add a new search provider in seconds.

Please make sure your PR passes all linter checks (`ruff check .`) and unit tests (`pytest tests/`) before submitting.
```

# SECURITY.md

```md
# Security Policy

## Supported Versions

Currently, only the latest release of the Reddit MCP Server is supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please do not disclose it publicly. 

Instead, please send an email to the repository owner or use the GitHub Security Advisories feature to privately report the issue. We will strive to respond within 48 hours and release a patch as quickly as possible.

## Secret Scanning

This repository utilizes GitHub's native Secret Scanning. Please ensure you do not commit any personal API keys, Reddit app credentials, or tokens. If a secret is accidentally pushed, GitHub will notify you. However, you should consider any pushed secret compromised and revoke it immediately.

```

# src/reddit_mcp/__init__.py

```py
# Reddit MCP Server package

```

# src/reddit_mcp/application/__init__.py

```py
# Application Layer
# This layer contains use cases, tool routing definitions, and schema validation.
# It orchestrates the domain layer and interfaces with the outside world.

```

# src/reddit_mcp/application/tools.py

```py
import logging
from typing import List, Literal, Optional

from reddit_mcp.domain.models import (
    RedditPost, RedditThread, MetaContext,
    PaginatedPostResponse, PaginatedCommentResponse
)
from reddit_mcp.infrastructure.reddit_client import RedditClient, RedditClientError
from reddit_mcp.infrastructure.auth import RedditAuthManager
from reddit_mcp.infrastructure.http import ResilientHTTPClient
from reddit_mcp.infrastructure.search.providers.duckduckgo import DuckDuckGoSearchProvider
from reddit_mcp.application.utils import llm_timeout, build_meta_context, is_high_quality_comment

logger = logging.getLogger(__name__)

class DependencyContainer:
    """Simple container for lazy-loading and injecting dependencies."""
    _reddit_client: Optional[RedditClient] = None

    @classmethod
    def get_reddit_client(cls) -> RedditClient:
        if cls._reddit_client is None:
            from reddit_mcp.infrastructure.settings import get_settings
            settings = get_settings()
            user_agent = settings.reddit_user_agent
            auth_manager = RedditAuthManager(user_agent=user_agent)
            http_client = ResilientHTTPClient(auth_manager=auth_manager, user_agent=user_agent)
            search_provider = DuckDuckGoSearchProvider()
            cls._reddit_client = RedditClient(http_client=http_client, search_provider=search_provider)
        return cls._reddit_client

    @classmethod
    def override_reddit_client(cls, client: RedditClient) -> None:
        """Used for injecting mock clients during testing."""
        cls._reddit_client = client

@llm_timeout(timeout_seconds=15)
async def search_knowledge(
    query: str,
    subreddit: Optional[str] = None,
    time_filter: Literal["all", "day", "week", "month", "year"] = "all",
    limit: int = 10
) -> PaginatedPostResponse:
    """
    STEP 1: FOUNDATION SEARCH. Use this to find factual threads or technical explanations.
    This uses a broad web-search (DuckDuckGo) to find Reddit threads that Reddit's own search might miss.
    Note: Pagination is not supported for this specific tool.
    """
    logger.info(f"search_knowledge: query='{query}'")
    client = DependencyContainer.get_reddit_client()
    posts, _ = await client.search(
        query=query, subreddit=subreddit, time_filter=time_filter, limit=limit
    )
    # Filter: Ensure we don't send posts with empty titles or very low quality
    valid_posts = [p for p in posts if len(p.title) > 5]
    
    return PaginatedPostResponse(
        meta_context=build_meta_context(),
        data=valid_posts,
        next_page_token=None
    )

@llm_timeout(timeout_seconds=15)
async def explore_reddit_discussions(
    keyword: str,
    subreddit: Optional[str] = None,
    sort: Literal["relevance", "hot", "top", "new", "comments"] = "relevance",
    time_filter: Literal["all", "day", "week", "month", "year"] = "year",
    limit: int = 10,
    page_token: Optional[str] = None
) -> PaginatedPostResponse:
    """
    STEP 2: SENTIMENT EXPLORATION. Use this to gauge public opinion and market acceptance.
    Always check `upvote_ratio`: >0.8 = Positive, ~0.5 = Controversial.
    Check `age_in_days` to ensure relevance. Use `next_page_token` to see more results.
    """
    logger.info(f"explore_reddit_discussions: keyword='{keyword}'")
    client = DependencyContainer.get_reddit_client()
    posts, next_token = await client.native_reddit_search(
        query=keyword, subreddit=subreddit, sort=sort, time_filter=time_filter, limit=limit, after=page_token
    )
    return PaginatedPostResponse(
        meta_context=build_meta_context(),
        data=posts,
        next_page_token=next_token
    )

@llm_timeout(timeout_seconds=20)
async def extract_public_opinion(
    post_url: str,
    max_comments: int = 30
) -> PaginatedCommentResponse:
    """
    DEEP DIVE TOOL: Use this ONLY after finding a relevant post via search tools.
    This tool extracts PURE human opinions, filtering out noise, bots, and low-effort content.
    Citations: You MUST use the `comment_url` for each specific quote in your final report.
    """
    logger.info(f"extract_public_opinion: url='{post_url}'")
    client = DependencyContainer.get_reddit_client()
    
    # Fetch thread (The client already maps basic data)
    thread = await client.get_post_thread(post_url=post_url, max_comments=max_comments)
    
    # Application Layer Filtering: Drop low quality before responding
    # This saves tokens and ensures the LLM only sees valuable input.
    refined_comments = [
        c for c in thread.comments 
        if is_high_quality_comment(author=c.author, body=c.body, score=c.score)
    ]
        
    return PaginatedCommentResponse(
        meta_context=build_meta_context(),
        data=refined_comments
    )

@llm_timeout(timeout_seconds=15)
async def analyze_niche_trends(
    subreddit_name: str,
    trend_type: Literal["hot", "new", "top", "rising"] = "rising",
    limit: int = 10,
    page_token: Optional[str] = None
) -> PaginatedPostResponse:
    """
    Use this tool when asked to suggest ideas, find pain points, or discover opportunities in a specific niche (e.g., 'SaaS', 'Entrepreneur').
    By looking at 'rising' or 'hot' posts, you can identify what problems users are actively struggling with RIGHT NOW.
    Always compare the post's `created_at` with the `current_server_date` provided in `meta_context`.
    """
    logger.info(f"analyze_niche_trends: subreddit='{subreddit_name}'")
    client = DependencyContainer.get_reddit_client()
    posts, next_token = await client.get_subreddit_trends(
        subreddit=subreddit_name, category=trend_type, limit=limit, after=page_token
    )
    return PaginatedPostResponse(
        meta_context=build_meta_context(),
        data=posts,
        next_page_token=next_token
    )

```

# src/reddit_mcp/application/utils.py

```py
import asyncio
import functools
import logging
from datetime import datetime, timezone
from typing import Callable, Any

logger = logging.getLogger(__name__)

def truncate_text(text: str | None, max_length: int = 2000) -> str:
    """
    Truncates text to a maximum length to prevent context window overflow.
    Intelligently cuts off text and appends '... (truncated)'.
    """
    if not text:
        return ""
    if len(text) > max_length:
        return text[:max_length] + "... (truncated)"
    return text

def calculate_age_in_days(created_utc: float | None) -> int:
    """Calculates the integer age of a post in days relative to now."""
    if not created_utc:
        return 0
    now = datetime.now(timezone.utc)
    created_dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    delta = now - created_dt
    return max(0, delta.days)

def format_timestamp(created_utc: float | None) -> str:
    """Converts Reddit's Unix timestamp to a human-readable string."""
    if not created_utc:
        return "Unknown date"
    dt = datetime.fromtimestamp(created_utc, tz=timezone.utc)
    return dt.strftime("%B %d, %Y")

def build_meta_context() -> dict:
    """Builds a rich temporal and operational context for the AI."""
    now = datetime.now(timezone.utc)
    return {
        "current_server_date": now.strftime("%A, %B %d, %Y"),
        "instruction_note": (
            "1. Use age_in_days for freshness analysis. 2. Use comment_url for citations. "
            "3. If next_page_token is present, you can request the next page. "
            "4. Only high-quality data is returned."
        )
    }

def build_comment_url(subreddit: str, post_id: str, comment_id: str) -> str:
    """Fabricates an absolute deep-link to a specific comment."""
    clean_sub = subreddit.replace('r/', '').replace('/r/', '')
    return f"https://www.reddit.com/r/{clean_sub}/comments/{post_id}/_/{comment_id}/"

def is_high_quality_comment(author: str, body: str, score: int, min_score: int = 2, min_length: int = 40) -> bool:
    """Smart heuristics to filter out bots, low-effort replies, and heavily downvoted opinions."""
    if not body or not author:
        return False
        
    author_lower = author.lower()
    if "bot" in author_lower or author_lower == "automoderator":
        return False
        
    if "i am a bot" in body.lower() or "action was performed automatically" in body.lower():
        return False
        
    if len(body.strip()) < min_length:
        return False
        
    if score < min_score:
        return False
        
    return True

def llm_timeout(timeout_seconds: int = 15):
    """
    Decorator that enforces a strict timeout on tool execution to prevent LLM client disconnects.
    Returns a graceful JSON fallback message for the LLM instead of throwing an unhandled exception.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> dict:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=timeout_seconds)
            except asyncio.TimeoutError:
                logger.warning(f"Tool {func.__name__} timed out after {timeout_seconds}s.")
                return {
                    "meta_context": build_meta_context(),
                    "data": [],
                    "next_page_token": None,
                    "status": "partial_timeout",
                    "message": "Request paused to prevent timeout. Use available data or retry."
                }
        return wrapper
    return decorator

```

# src/reddit_mcp/domain/__init__.py

```py
# Domain Layer
# This layer contains the core business logic and Pydantic data models.
# It should have zero dependencies on other layers.

```

# src/reddit_mcp/domain/models.py

```py
from pydantic import BaseModel, Field
from typing import List, Optional

class RedditPost(BaseModel):
    """Represents a single Reddit post with time-awareness."""
    id: str = Field(..., description="The unique identifier of the post.")
    title: str = Field(..., description="The title of the post.")
    subreddit: str = Field(..., description="The name of the subreddit where this was posted.")
    score: int = Field(..., description="The net upvotes.")
    upvote_ratio: float = Field(0.0, description="Consensus metric: 1.0 = Loved, 0.5 = Controversial.")
    num_comments: int = Field(..., description="Total comments.")
    url: str = Field(..., description="The direct URL to the post.")
    age_in_days: int = Field(..., description="Days since post was created. 0 means posted today.")
    created_at_human: str = Field(..., description="Human-readable date (e.g., 'October 15, 2023').")
    text_preview: str = Field(..., description="A short preview of the post body.")

class RedditComment(BaseModel):
    """Represents a high-quality filtered comment."""
    id: str = Field(..., description="The comment identifier.")
    author: str = Field(..., description="The author's username.")
    score: int = Field(..., description="Net upvotes.")
    body: str = Field(..., description="Markdown content.")
    comment_url: str = Field(..., description="Direct citation link. Use this for references.")
    created_at_human: str = Field(..., description="Human-readable date.")

class RedditThread(BaseModel):
    """Represents a full Reddit thread, including the main post and its top comments."""
    post: RedditPost = Field(..., description="The original Reddit post.")
    comments: List[RedditComment] = Field(..., description="A list of comments associated with the post.")

class MetaContext(BaseModel):
    """Temporal and instructional context for the AI."""
    current_server_date: str = Field(..., description="The current server date.")
    instruction_note: str = Field(..., description="Guiding instruction for the LLM.")

class PaginatedPostResponse(BaseModel):
    """A paginated list of Reddit posts wrapped with meta-context."""
    meta_context: MetaContext = Field(..., description="Temporal and spatial context for the AI.")
    data: List[RedditPost] = Field(..., description="The extracted posts.")
    next_page_token: Optional[str] = Field(None, description="Pass this token to the tool again to fetch the next page.")
    status: str = Field("success", description="Status of the request (e.g., success, partial_timeout).")
    message: Optional[str] = Field(None, description="System message or warning (especially if partial_timeout occurred).")

class PaginatedCommentResponse(BaseModel):
    """A list of comments wrapped with meta-context."""
    meta_context: MetaContext = Field(..., description="Temporal and spatial context for the AI.")
    data: List[RedditComment] = Field(..., description="The extracted comments.")
    status: str = Field("success", description="Status of the request.")
    message: Optional[str] = Field(None, description="System message or warning.")

```

# src/reddit_mcp/infrastructure/__init__.py

```py
# Infrastructure Layer
# This layer contains external dependencies, such as HTTP clients (httpx),
# rate limiters, database connections, and logging configuration.

```

# src/reddit_mcp/infrastructure/auth.py

```py
import asyncio
import base64
import logging
import time
from typing import Optional

import httpx
from reddit_mcp.infrastructure.settings import get_settings

logger = logging.getLogger(__name__)

class RedditAuthError(Exception):
    """Exception raised for errors during Reddit authentication."""
    pass

class RedditAuthManager:
    """
    Manages OAuth 2.0 Access Tokens for Reddit via the client_credentials flow.
    Automatically fetches and caches the token, refreshing it before it expires.
    """
    def __init__(self, user_agent: str):
        settings = get_settings()
        self.client_id = settings.reddit_client_id
        self.client_secret = settings.reddit_client_secret
        self.user_agent = user_agent

        self._token: Optional[str] = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    async def get_token(self) -> str:
        """
        Get a valid access token, refreshing it if necessary.
        """
        async with self._lock:
            # Refresh if token is missing or expires within the next 30 seconds
            if not self._token or time.time() >= (self._expires_at - 30):
                await self._refresh_token()
            
            return self._token

    async def _refresh_token(self) -> None:
        """
        Fetch a new token from Reddit API using client credentials.
        """
        logger.info("Fetching new Reddit OAuth access token...")
        
        auth_string = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "User-Agent": self.user_agent,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://www.reddit.com/api/v1/access_token",
                    headers=headers,
                    data=data,
                    timeout=10.0
                )
                response.raise_for_status()
                
                token_data = response.json()
                self._token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)
                
                if not self._token:
                    raise RedditAuthError("Token response did not contain an access_token")
                    
                self._expires_at = time.time() + expires_in
                logger.info("Successfully acquired new Reddit OAuth access token.")
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to fetch token. HTTP Status: {e.response.status_code}. Body: {e.response.text}")
                raise RedditAuthError(f"HTTP {e.response.status_code} during token refresh") from e
            except httpx.RequestError as e:
                logger.error(f"Network error during token refresh: {e}")
                raise RedditAuthError(f"Network error: {e}") from e
            except Exception as e:
                logger.error(f"Unexpected error during token refresh: {e}")
                raise RedditAuthError(f"Unexpected error: {e}") from e

```

# src/reddit_mcp/infrastructure/http.py

```py
import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

from reddit_mcp.infrastructure.auth import RedditAuthManager

logger = logging.getLogger(__name__)

class RedditRateLimitError(Exception):
    """Exception raised when the maximum number of rate limit retries is exceeded."""
    pass

class ResilientHTTPClient:
    """
    HTTP client wrapper using httpx with built-in resilience.
    Automatically injects Reddit OAuth tokens, enforces User-Agent,
    and handles rate limits (429) using exponential backoff.
    """
    def __init__(self, auth_manager: RedditAuthManager, user_agent: str):
        self.auth_manager = auth_manager
        self.user_agent = user_agent
        self.client = httpx.AsyncClient(timeout=15.0)

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 3) -> httpx.Response:
        """
        Perform a GET request with automatic token injection and rate limit retries.
        """
        for attempt in range(max_retries):
            token = await self.auth_manager.get_token()
            
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": self.user_agent,
            }
            
            try:
                response = await self.client.get(url, params=params, headers=headers)
                
                # Check for rate limit (429) or Server Errors (500, 502, 503, 504)
                if response.status_code == 429 or response.status_code >= 500:
                    retry_after = response.headers.get("Retry-After")
                    
                    if response.status_code == 429 and retry_after and retry_after.isdigit():
                        wait_seconds = int(retry_after)
                    else:
                        # Exponential backoff for 5xx or missing Retry-After
                        wait_seconds = 2 ** attempt
                        
                    logger.warning(
                        f"HTTP {response.status_code} on {url}. Retrying in {wait_seconds} seconds. "
                        f"(Attempt {attempt + 1}/{max_retries})"
                    )
                    
                    if attempt < max_retries - 1:
                        await asyncio.sleep(wait_seconds)
                        continue
                    else:
                        if response.status_code == 429:
                            raise RedditRateLimitError("Max retries exceeded due to rate limiting.")
                        else:
                            response.raise_for_status()
                
                # Raise for other HTTP errors (4xx)
                response.raise_for_status()
                return response
                
            except httpx.HTTPStatusError as e:
                # Handled retries above, raise if we get here
                raise e
            except httpx.RequestError as e:
                logger.error(f"Network error on {url}: {e}")
                if attempt < max_retries - 1:
                    wait_seconds = 2 ** attempt
                    await asyncio.sleep(wait_seconds)
                    continue
                raise e
        
        raise RuntimeError("Failed to complete request (should not reach here)")

```

# src/reddit_mcp/infrastructure/logging.py

```py
import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    """
    Configures the root logger to output strictly to stderr.
    
    This is a critical requirement for MCP servers using standard I/O transport.
    If logs are written to stdout, they will corrupt the JSON-RPC communication
    between the MCP server and the client.
    
    Args:
        level: The logging level to set (e.g., logging.INFO, logging.DEBUG)
    """
    # Create a handler that writes exclusively to stderr
    handler = logging.StreamHandler(sys.stderr)
    
    # Define a clear format for the logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to prevent duplicate logs or stdout leakage
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
    
    # Ensure our own package logger is also explicitly set
    logger = logging.getLogger("reddit_mcp")
    logger.setLevel(level)
    
    logger.debug("Logging initialized (stderr only).")

```

# src/reddit_mcp/infrastructure/reddit_client.py

```py
import logging
import re
from typing import Dict, Any, List, Optional, Tuple

from reddit_mcp.domain.models import RedditPost, RedditComment, RedditThread
from reddit_mcp.application.utils import truncate_text, format_timestamp, build_comment_url
from reddit_mcp.infrastructure.http import ResilientHTTPClient
from reddit_mcp.infrastructure.search.base import BaseSearchProvider

logger = logging.getLogger(__name__)

class RedditClientError(Exception):
    """Base exception for Reddit client errors."""
    pass

class RedditClient:
    """
    Asynchronous client for interacting with the Reddit API using a resilient HTTP client.
    """
    def __init__(self, http_client: ResilientHTTPClient, search_provider: BaseSearchProvider):
        self.http_client = http_client
        self.search_provider = search_provider

    async def close(self):
        """Close underlying resources."""
        await self.http_client.close()

    def _map_submission(self, data: Dict[str, Any]) -> RedditPost:
        """Map Reddit JSON submission data to our enriched RedditPost model."""
        created_utc = data.get("created_utc")
        from reddit_mcp.application.utils import calculate_age_in_days
        
        return RedditPost(
            id=data.get("id", ""),
            title=data.get("title", ""),
            subreddit=data.get("subreddit", ""),
            score=data.get("score", 0),
            upvote_ratio=data.get("upvote_ratio", 0.0),
            num_comments=data.get("num_comments", 0),
            url=f"https://www.reddit.com{data.get('permalink', '')}",
            age_in_days=calculate_age_in_days(created_utc),
            created_at_human=format_timestamp(created_utc),
            text_preview=truncate_text(data.get("selftext", ""), 500)
        )

    def _map_comment(self, data: Dict[str, Any], post_id: str, subreddit: str) -> Optional[RedditComment]:
        """Map Reddit JSON comment data to our refined RedditComment model."""
        body = data.get("body")
        if not body:
            return None
            
        comment_id = data.get("id", "")
        return RedditComment(
            id=comment_id,
            author=data.get("author", "[deleted]"),
            score=data.get("score", 0),
            body=truncate_text(body, 2000),
            comment_url=build_comment_url(subreddit, post_id, comment_id),
            created_at_human=format_timestamp(data.get("created_utc"))
        )

    def _extract_post_id(self, url: str) -> Optional[str]:
        """Extract the Reddit post ID from a standard URL."""
        match = re.search(r"/comments/([a-z0-9]+)", url)
        return match.group(1) if match else None

    async def get_subreddit_trends(
        self, 
        subreddit: str, 
        category: str = "hot", 
        time_filter: str = "all", 
        limit: int = 10,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """Fetch trending posts from a subreddit."""
        subreddit = subreddit.strip()
        if subreddit.startswith("/r/"):
            subreddit = subreddit[3:]
        elif subreddit.startswith("r/"):
            subreddit = subreddit[2:]
            
        url = f"https://oauth.reddit.com/r/{subreddit}/{category}.json"
        params = {"limit": limit, "t": time_filter}
        if after:
            params["after"] = after
        if before:
            params["before"] = before

        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            new_after = data.get("data", {}).get("after")
            return posts, new_after
        except Exception as e:
            raise RedditClientError(f"Error fetching subreddit trends: {e}")

    async def get_post_thread(self, post_url: str, max_comments: int = 50) -> RedditThread:
        """Fetch a specific post and its top comments, parsing the comment tree."""
        post_id = self._extract_post_id(post_url)
        if not post_id:
            raise RedditClientError("Invalid Reddit post URL provided.")
            
        url = f"https://oauth.reddit.com/comments/{post_id}.json"
        params = {"limit": max_comments + 20} # Buffer for 'more' items
        
        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            if not isinstance(data, list) or len(data) < 2:
                raise RedditClientError("Unexpected response format from Reddit API.")
                
            post_data = data[0]["data"]["children"][0]["data"]
            post = self._map_submission(post_data)
            
            comments = []
            comment_children = data[1].get("data", {}).get("children", [])
            
            def parse_comments(children: List[Dict[str, Any]]):
                for child in children:
                    if len(comments) >= max_comments:
                        return
                        
                    kind = child.get("kind")
                    c_data = child.get("data", {})
                    
                    if kind == "t1": # Comment
                        mapped = self._map_comment(c_data, post.id, post.subreddit)
                        if mapped:
                            comments.append(mapped)
                            
                        # Recursively parse replies if they exist
                        replies = c_data.get("replies")
                        if isinstance(replies, dict):
                            parse_comments(replies.get("data", {}).get("children", []))
                            
                    elif kind == "more":
                        # We ignore 'more' comments to avoid excessive API requests.
                        # This guarantees we only use the comments returned in the initial payload.
                        continue

            parse_comments(comment_children)
            
            return RedditThread(post=post, comments=comments)
        except Exception as e:
            raise RedditClientError(f"Error fetching thread: {e}")

    async def native_reddit_search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 10,
        after: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """Search using Reddit's official API. Ideal for metrics like upvote_ratio and native sorting."""
        url = "https://oauth.reddit.com/search.json"
        params = {
            "q": query,
            "sort": sort,
            "t": time_filter,
            "limit": limit
        }
        if subreddit:
            url = f"https://oauth.reddit.com/r/{subreddit}/search.json"
            params["restrict_sr"] = True
        if after:
            params["after"] = after

        try:
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            new_after = data.get("data", {}).get("after")
            return posts, new_after
        except Exception as e:
            raise RedditClientError(f"Error during native Reddit search: {e}")

    async def search(
        self, 
        query: str, 
        subreddit: Optional[str] = None, 
        sort: str = "relevance", 
        time_filter: str = "all", 
        limit: int = 10,
        after: Optional[str] = None,
        before: Optional[str] = None
    ) -> Tuple[List[RedditPost], Optional[str]]:
        """
        Search Reddit using the injected SearchProvider (e.g. DDG).
        Useful for general knowledge finding where native search fails.
        """
        try:
            search_results = await self.search_provider.search(
                query=query, 
                subreddit=subreddit, 
                time_filter=time_filter, 
                limit=limit
            )
            
            if not search_results:
                return [], None
                
            post_ids = []
            for res in search_results:
                if hasattr(res, 'post_id') and res.post_id:
                    post_ids.append(f"t3_{res.post_id}")
                    
            if not post_ids:
                return [], None
                
            url = "https://oauth.reddit.com/api/info.json"
            params = {"id": ",".join(post_ids)}
            
            response = await self.http_client.get(url, params=params)
            data = response.json()
            
            posts = []
            for child in data.get("data", {}).get("children", []):
                if child.get("kind") == "t3":
                    posts.append(self._map_submission(child["data"]))
                    
            # Search providers like DDG don't natively return Reddit pagination tokens
            return posts, None
            
        except Exception as e:
            raise RedditClientError(f"Error during web search: {e}")

```

# src/reddit_mcp/infrastructure/search/__init__.py

```py
from reddit_mcp.infrastructure.search.base import BaseSearchProvider, SearchResult
from reddit_mcp.infrastructure.search.providers.duckduckgo import DuckDuckGoSearchProvider, RedditSearchResult

__all__ = [
    "BaseSearchProvider",
    "SearchResult",
    "DuckDuckGoSearchProvider",
    "RedditSearchResult"
]

```

# src/reddit_mcp/infrastructure/search/base.py

```py
from abc import ABC, abstractmethod
from typing import List, Optional

class SearchResult:
    """A generic search result."""
    def __init__(self, url: str, title: str, snippet: str) -> None:
        self.url = url
        self.title = title
        self.snippet = snippet

class BaseSearchProvider(ABC):
    """
    Abstract base class for search engine providers.
    Follows the Strategy Pattern to allow easy addition of new search engines.
    """
    
    @abstractmethod
    async def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        time_filter: str = "all",
        limit: int = 10,
    ) -> List[SearchResult]:
        """
        Execute a search query and return a list of SearchResults.
        """
        pass

```

# src/reddit_mcp/infrastructure/search/providers/__init__.py

```py

```

# src/reddit_mcp/infrastructure/search/providers/duckduckgo.py

```py
import asyncio
import logging
import re
from typing import List, Optional

from ddgs import DDGS

from reddit_mcp.infrastructure.search.base import BaseSearchProvider, SearchResult

logger = logging.getLogger(__name__)

class RedditSearchResult(SearchResult):
    """A search result specifically parsed for Reddit URLs."""
    
    @property
    def post_id(self) -> str:
        """Extract the Reddit post ID from the URL, if present."""
        match = re.search(r"/comments/([a-z0-9]+)", self.url)
        return match.group(1) if match else ""

    @property
    def subreddit(self) -> str:
        """Extract the subreddit name from the URL, if present."""
        match = re.search(r"/r/([a-zA-Z0-9_]+)", self.url)
        return match.group(1) if match else ""

class DuckDuckGoSearchProvider(BaseSearchProvider):
    """
    Asynchronous client for searching Reddit using DuckDuckGo's 'site:' operator.
    This provides a more robust search than Reddit's internal search for general queries.
    """
    
    async def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        time_filter: str = "all",
        limit: int = 10,
    ) -> List[RedditSearchResult]:
        """
        Searches Reddit using DuckDuckGo.
        Returns a list of RedditSearchResult objects pointing to Reddit threads.
        """
        if subreddit:
            subreddit = subreddit.strip()
            if subreddit.startswith("/r/"):
                subreddit = subreddit[3:]
            elif subreddit.startswith("r/"):
                subreddit = subreddit[2:]
            site_filter = f"site:reddit.com/r/{subreddit}"
        else:
            site_filter = "site:reddit.com"

        full_query = f"{site_filter} {query}"

        logger.info(f"DDG Search Query: {full_query}")

        timelimit = None
        if time_filter == "day":
            timelimit = "d"
        elif time_filter == "week":
            timelimit = "w"
        elif time_filter == "month":
            timelimit = "m"
        elif time_filter == "year":
            timelimit = "y"

        try:
            def _search() -> List[dict]:
                with DDGS() as ddgs:
                    return list(ddgs.text(full_query, timelimit=timelimit, max_results=limit))

            results = await asyncio.to_thread(_search)
        except Exception as e:
            logger.error(f"Error during DuckDuckGo search: {e}")
            return []

        urls: List[RedditSearchResult] = []
        for res in results:
            url = res.get("href", "")
            if "reddit.com" in url:
                urls.append(RedditSearchResult(
                    url=url,
                    title=res.get("title", ""),
                    snippet=res.get("body", ""),
                ))
        return urls

```

# src/reddit_mcp/infrastructure/search/providers/README.md

```md
# Search Providers

This directory contains the integration logic for various search engines. 
By default, we use **DuckDuckGo** as it doesn't require an API key and performs well for `.reddit.com` searches.

## 🤝 How to contribute a new Search Provider

Want to add Google Search, Tavily, or Bing? It's extremely easy:
1. Create a new file in this directory (e.g., `google_search.py`).
2. Import the base class: `from reddit_mcp.infrastructure.search.base import BaseSearchProvider, SearchResult`.
3. Create your class and make it inherit from `BaseSearchProvider`.
4. Implement the async `search()` method.
5. Update `src/reddit_mcp/application/tools.py` to use your new provider!
```

# src/reddit_mcp/infrastructure/settings.py

```py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class AppConfig(BaseSettings):
    """
    Centralized configuration for the Reddit MCP Server.
    Validates environment variables at startup (Fail-Fast).
    """
    reddit_client_id: str = Field(..., description="Reddit App Client ID")
    reddit_client_secret: str = Field(..., description="Reddit App Client Secret")
    reddit_user_agent: str = Field(
        default="reddit-mcp-server/0.1.0 (by /u/reddit-mcp-server-dev)", 
        description="User-Agent string for HTTP requests"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> AppConfig:
    """
    Returns a cached instance of the application settings.
    Will raise a ValidationError immediately if required vars are missing.
    """
    return AppConfig()
```

# src/reddit_mcp/interface/__init__.py

```py
# Interface Layer
# This layer handles the external presentation and protocol communication.
# For MCP, this is where the FastMCP server is configured and where STDIO transport
# is initialized.

```

# src/reddit_mcp/interface/server.py

```py
# pyrefly: ignore [missing-import]
from fastmcp import FastMCP
import logging

from reddit_mcp.application.tools import (
    search_knowledge,
    explore_reddit_discussions,
    extract_public_opinion,
    analyze_niche_trends
)

logger = logging.getLogger(__name__)

def create_server() -> FastMCP:
    """
    Creates and configures the FastMCP server instance.
    
    This server handles the Model Context Protocol (MCP) JSON-RPC messages.
    It sits in the interface layer and will route requests to the application layer.
    
    Returns:
        A configured FastMCP instance ready to be run.
    """
    logger.info("Initializing Reddit MCP Server (AI-Native Edition)")
    
    # Initialize the FastMCP server with dependencies
    mcp = FastMCP(
        name="Reddit MCP Server"
    )
    
    # Register tools from the application layer
    mcp.tool()(search_knowledge)
    mcp.tool()(explore_reddit_discussions)
    mcp.tool()(extract_public_opinion)
    mcp.tool()(analyze_niche_trends)
    logger.debug("FastMCP server initialized with AI-Native tools.")
    
    return mcp

```

# src/reddit_mcp/main.py

```py
import logging
import sys
import asyncio

from reddit_mcp.infrastructure.logging import setup_logging
from reddit_mcp.interface.server import create_server
from reddit_mcp.application.tools import DependencyContainer

def main():
    """
    Main entry point for the Reddit MCP Server.
    
    This script initializes the strict stderr logging configuration to prevent
    JSON-RPC stream corruption, sets up the server, and starts the STDIO transport.
    """
    # 1. Initialize strictly to stderr
    setup_logging(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Reddit MCP Server...")
        
        # 2. Create the FastMCP server instance
        mcp = create_server()
        
        # 3. Start the standard IO (STDIO) transport loop.
        # FastMCP's run() uses STDIO by default in production.
        logger.info("Starting STDIO transport loop. Listening for JSON-RPC messages.")
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error encountered: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Cleaning up resources...")
        try:
            client = DependencyContainer.get_reddit_client()
            asyncio.run(client.close())
        except Exception as cleanup_error:
            logger.error(f"Error during cleanup: {cleanup_error}")
            
if __name__ == "__main__":
    main()

```

# tests/test_auth.py

```py
import pytest
import os
from unittest.mock import AsyncMock, patch
import httpx
from pydantic import ValidationError
from reddit_mcp.infrastructure.auth import RedditAuthManager, RedditAuthError
from reddit_mcp.infrastructure.settings import get_settings

@pytest.fixture
def auth_env(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "dummy_secret")
    get_settings.cache_clear()

@pytest.mark.asyncio
async def test_auth_manager_missing_env():
    # Ensure env is clear to test the missing credentials error
    with patch.dict(os.environ, clear=True):
        get_settings.cache_clear()
        # Force pydantic-settings to believe the .env file does not exist
        with patch("pathlib.Path.is_file", return_value=False):
            with pytest.raises(ValidationError, match="reddit_client_id"):
                RedditAuthManager(user_agent="test")

from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_auth_manager_success(auth_env):
    manager = RedditAuthManager(user_agent="test")
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "mock_token", "expires_in": 3600}
    mock_response.raise_for_status = MagicMock()
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        token = await manager.get_token()
        
    assert token == "mock_token"

@pytest.mark.asyncio
async def test_auth_manager_http_error(auth_env):
    manager = RedditAuthManager(user_agent="test")
    
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Unauthorized", request=MagicMock(), response=mock_response
    )
    
    with patch("httpx.AsyncClient.post", return_value=mock_response):
        with pytest.raises(RedditAuthError, match="HTTP 401"):
            await manager.get_token()
```

# tests/test_http.py

```py
import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.infrastructure.http import ResilientHTTPClient, RedditRateLimitError
from reddit_mcp.infrastructure.auth import RedditAuthManager

@pytest.fixture
def mock_auth_manager():
    manager = MagicMock(spec=RedditAuthManager)
    manager.get_token = AsyncMock(return_value="mock_token")
    return manager

@pytest.mark.asyncio
async def test_http_client_success(mock_auth_manager):
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    
    client.client.get = AsyncMock(return_value=mock_response)
    
    response = await client.get("http://test.com")
    assert response.status_code == 200
    assert client.client.get.call_count == 1
    await client.close()

@pytest.mark.asyncio
async def test_http_client_429_retry_success(mock_auth_manager, monkeypatch):
    # Skip actual asyncio.sleep during tests to make them fast
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    fail_response = MagicMock()
    fail_response.status_code = 429
    fail_response.headers = {"Retry-After": "1"}
    
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.raise_for_status = MagicMock()
    
    # First call returns 429, second call returns 200
    client.client.get = AsyncMock(side_effect=[fail_response, success_response])
    
    response = await client.get("http://test.com", max_retries=3)
    assert response.status_code == 200
    assert client.client.get.call_count == 2
    await client.close()

@pytest.mark.asyncio
async def test_http_client_429_max_retries(mock_auth_manager, monkeypatch):
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    client = ResilientHTTPClient(auth_manager=mock_auth_manager, user_agent="test")
    
    fail_response = MagicMock()
    fail_response.status_code = 429
    fail_response.headers = {"Retry-After": "1"}
    
    # Always return 429
    client.client.get = AsyncMock(return_value=fail_response)
    
    with pytest.raises(RedditRateLimitError, match="Max retries exceeded"):
        await client.get("http://test.com", max_retries=2)
        
    assert client.client.get.call_count == 2
    await client.close()
```

# tests/test_reddit_client.py

```py
import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.infrastructure.reddit_client import RedditClient, RedditClientError
from reddit_mcp.domain.models import RedditPost, RedditThread, RedditComment

@pytest.fixture
def mock_http_client():
    client = MagicMock()
    client.get = AsyncMock()
    return client

@pytest.fixture
def mock_search_provider():
    provider = MagicMock()
    provider.search = AsyncMock()
    return provider

@pytest.fixture
def reddit_client(mock_http_client, mock_search_provider):
    return RedditClient(http_client=mock_http_client, search_provider=mock_search_provider)

@pytest.mark.asyncio
async def test_get_subreddit_trends_success(reddit_client, mock_http_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": {
            "after": "t3_abc",
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "123",
                        "title": "Test Post",
                        "subreddit": "test",
                        "score": 100,
                        "upvote_ratio": 0.95,
                        "num_comments": 10,
                        "permalink": "/r/test/comments/123/",
                        "created_utc": 1700000000.0,
                        "selftext": "Hello world text"
                    }
                }
            ]
        }
    }
    mock_http_client.get.return_value = mock_response

    posts, next_token = await reddit_client.get_subreddit_trends("test", "hot")
    
    assert len(posts) == 1
    post = posts[0]
    assert post.age_in_days >= 0
    assert "created_at_human" in post.model_dump()
    assert post.text_preview == "Hello world text"

@pytest.mark.asyncio
async def test_get_post_thread_success(reddit_client, mock_http_client):
    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"data": {"children": [{"kind": "t3", "data": {
            "id": "123", "title": "Post", "subreddit": "test", "score": 10, 
            "upvote_ratio": 1.0, "num_comments": 1, "permalink": "/r/test/comments/123/", 
            "created_utc": 1700000000.0, "selftext": "..."
        }}]}},
        {"data": {"children": [{"kind": "t1", "data": {
            "id": "c1", "author": "user1", "score": 5, "body": "Comment body", "created_utc": 1700000050.0
        }}]}}
    ]
    mock_http_client.get.return_value = mock_response
    
    thread = await reddit_client.get_post_thread("http://reddit.com/r/test/comments/123")
    
    assert isinstance(thread, RedditThread)
    assert thread.comments[0].created_at_human is not None

@pytest.mark.asyncio
async def test_get_post_thread_malformed_json(reddit_client, mock_http_client):
    # Simulate reddit returning an unexpected structure (e.g., dict instead of list)
    mock_response = MagicMock()
    mock_response.json.return_value = {"error": 404}
    mock_http_client.get.return_value = mock_response
    
    with pytest.raises(RedditClientError, match="Unexpected response format"):
        await reddit_client.get_post_thread("http://reddit.com/r/test/comments/123")
```

# tests/test_tools.py

```py
import pytest
from unittest.mock import AsyncMock, MagicMock
from reddit_mcp.application import tools
from reddit_mcp.application.tools import DependencyContainer
import asyncio
from reddit_mcp.domain.models import (
    PaginatedPostResponse, 
    PaginatedCommentResponse, 
    RedditPost, 
    RedditComment, 
    RedditThread
)
from reddit_mcp.application.utils import truncate_text

@pytest.fixture
def sample_post():
    return RedditPost(
        id="123",
        title="Valid Test Post Title",
        subreddit="test",
        score=100,
        upvote_ratio=0.95,
        num_comments=10,
        url="https://reddit.com/r/test/comments/123",
        age_in_days=5,
        created_at_human="October 15, 2023",
        text_preview="Hello preview"
    )

@pytest.fixture(autouse=True)
def mock_reddit_client():
    mock_client = MagicMock()
    mock_client.search = AsyncMock()
    mock_client.native_reddit_search = AsyncMock()
    mock_client.get_subreddit_trends = AsyncMock()
    mock_client.get_post_thread = AsyncMock()
    DependencyContainer.override_reddit_client(mock_client)
    yield mock_client
    DependencyContainer._reddit_client = None

@pytest.mark.asyncio
async def test_search_knowledge_filters_short_titles(mock_reddit_client, sample_post):
    # Create a post with a very short title
    bad_post = sample_post.model_copy()
    bad_post.title = "Hi"
    
    mock_reddit_client.search.return_value = ([sample_post, bad_post], None)
    
    result = await tools.search_knowledge("query")
    
    # Should only return the valid_post
    assert len(result.data) == 1
    assert result.data[0].title == "Valid Test Post Title"

@pytest.mark.asyncio
async def test_extract_public_opinion_logic(mock_reddit_client, sample_post):
    # One high quality, one low quality (short)
    good_comment = RedditComment(
        id="c1", author="user1", score=10, body="This is a long enough and high quality comment for testing.",
        comment_url="url1", created_at_human="date"
    )
    bad_comment = RedditComment(
        id="c2", author="bot", score=-5, body="short",
        comment_url="url2", created_at_human="date"
    )
    
    mock_thread = RedditThread(post=sample_post, comments=[good_comment, bad_comment])
    mock_reddit_client.get_post_thread.return_value = mock_thread
    
    result = await tools.extract_public_opinion("http://url")
    
    # Should filter out the bad comment at application layer
    assert len(result.data) == 1
    assert result.data[0].id == "c1"
    assert "instruction_note" in result.meta_context.model_dump()

@pytest.mark.asyncio
async def test_explore_reddit_discussions_pagination(mock_reddit_client, sample_post):
    # Simulate reddit client returning a next_page_token
    mock_reddit_client.native_reddit_search.return_value = ([sample_post], "after_token_123")
    
    result = await tools.explore_reddit_discussions("keyword")
    
    assert len(result.data) == 1
    assert result.next_page_token == "after_token_123"

@pytest.mark.asyncio
async def test_search_knowledge_empty_results(mock_reddit_client):
    # Simulate an empty search result
    mock_reddit_client.search.return_value = ([], None)
    
    result = await tools.search_knowledge("nonexistent_query")
    
    assert len(result.data) == 0
    assert result.next_page_token is None

@pytest.mark.asyncio
async def test_tool_llm_timeout(monkeypatch):
    # We test the timeout by mocking asyncio.wait_for to raise a TimeoutError
    async def mock_wait_for(aw, timeout=None, **kwargs):
        aw.close()  # Close the unawaited coroutine to prevent RuntimeWarning
        raise asyncio.TimeoutError()
        
    monkeypatch.setattr(asyncio, "wait_for", mock_wait_for)
    
    result = await tools.search_knowledge("query")
    
    # It should not crash, but return a fallback dict
    assert isinstance(result, dict)
    assert result["status"] == "partial_timeout"
    assert "Request paused" in result["message"]
    assert len(result["data"]) == 0

def test_truncate_text_util():
    # Phase 4 Utils test
    long_text = "A" * 3000
    truncated = truncate_text(long_text, 2000)
    
    assert len(truncated) == 2000 + len("... (truncated)")
    assert truncated.endswith("... (truncated)")
    
    # Test empty
    assert truncate_text(None) == ""
    assert truncate_text("") == ""
```

