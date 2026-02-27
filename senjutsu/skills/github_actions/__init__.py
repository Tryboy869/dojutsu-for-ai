"""Built-in github-actions skill content."""

SKILL_CONTENT = '''---
name: github-actions
description: "Apply when generating CI/CD workflows, GitHub Actions, automated pipelines, testing automation, deployment, PyPI/npm publishing, Docker builds, or any .github/workflows YAML files."
---

# GITHUB ACTIONS — Production CI/CD Expert

## Core Philosophy
Every workflow must be: FAST · SECURE · RELIABLE · MAINTAINABLE

---

## ESSENTIAL WORKFLOW PATTERNS

### Python Package CI + PyPI Publish
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*']
  pull_request:
    branches: [main]

jobs:
  test:
    name: Test Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
    
    - name: Lint
      run: |
        ruff check .
        mypy --strict src/
    
    - name: Test with coverage
      run: |
        pytest tests/ -v --tb=short \
          --cov=src/ \
          --cov-report=xml \
          --cov-report=term-missing \
          --cov-fail-under=80
    
    - name: Upload coverage
      uses: codecov/codecov-action@v4
      if: matrix.python-version == '3.11'
      with:
        file: ./coverage.xml

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run Bandit
      run: |
        pip install bandit[toml]
        bandit -r src/ -c pyproject.toml
    - name: Check dependencies
      run: |
        pip install safety
        safety check

  publish-pypi:
    name: Publish to PyPI
    needs: [test, security]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment:
      name: pypi
      url: https://pypi.org/p/${{ env.PACKAGE_NAME }}
    permissions:
      id-token: write  # OIDC trusted publishing
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.11"
    
    - name: Build package
      run: |
        pip install build
        python -m build
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
```

---

## SECURITY BEST PRACTICES

### Secrets management:
```yaml
# ✅ CORRECT — use secrets
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh

# ❌ NEVER — hardcoded
- name: Deploy
  run: API_KEY=sk-real-key ./deploy.sh
```

### Permission minimization:
```yaml
permissions:
  contents: read      # NOT write unless pushing
  packages: write     # Only if publishing packages
  id-token: write     # Only for OIDC auth
```

### Pin action versions:
```yaml
# ✅ Pinned to SHA for security
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

# ⚠️ Tag only — acceptable for trusted actions
- uses: actions/checkout@v4
```

---

## CACHING STRATEGIES

```yaml
# Python dependencies
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: 'pip'

# Node modules
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

# Custom cache
- uses: actions/cache@v4
  with:
    path: ~/.cache/myapp
    key: ${{ runner.os }}-myapp-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-myapp-
```

---

## MATRIX STRATEGIES

```yaml
# Cross-platform testing
strategy:
  fail-fast: false  # Don't cancel all on first failure
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    python: ["3.9", "3.10", "3.11", "3.12"]
    exclude:
      - os: windows-latest
        python: "3.9"  # Known issue

# Include special cases
include:
  - os: ubuntu-latest
    python: "3.13-dev"
    experimental: true
```

---

## REUSABLE WORKFLOWS

```yaml
# .github/workflows/reusable-test.yml
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
    secrets:
      CODECOV_TOKEN:
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # ...
```

---

## NOTIFICATIONS AND REPORTING

```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ci-cd'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

- name: Create GitHub Release
  if: startsWith(github.ref, 'refs/tags/')
  uses: softprops/action-gh-release@v2
  with:
    generate_release_notes: true
    files: dist/*
```

---

## ANTI-PATTERNS TO AVOID

- ❌ `continue-on-error: true` on critical steps
- ❌ Running as root in containers
- ❌ Storing artifacts for > 30 days (cost)
- ❌ `run: pip install *` without pinned versions
- ❌ Not caching dependencies (slow builds)
- ❌ `pull_request_target` without careful review (security risk)
- ❌ Exposing secrets in logs (`echo $SECRET`)
'''
