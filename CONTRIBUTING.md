# Contributing to LLMPop

Thanks for your interest in contributing 🎉
This guide explains how to set up your environment, follow coding standards, and submit pull requests.

---

## 🚀 Getting Started

1. **Fork & clone the repo:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/llmpop.git
   cd llmpop
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   make install-dev
   ```

---

## 🛠️ Development Workflow

* **Lint & type check:**

  ```bash
  make lint
  ```

* **Auto-format code:**

  ```bash
  make fmt
  ```

* **Run tests:**

  ```bash
  make test
  ```

All lint, formatting, and tests must pass before submitting a pull request.

---

## ✅ Pre-Commit Checklist

Before you commit, please follow this checklist to keep the codebase clean, consistent, and chatbot-friendly.

### Manual updates (you do)

1. **Code & Public API**

   * Implement your changes in `src/llmpop/...`.
   * Export new/renamed public functions in `src/llmpop/__init__.py` via `__all__`.
   * If you added dependencies, update `pyproject.toml`.

2. **LLM\_READABLE\_GUIDE.md**

   * Update:

     * New/changed function names in **Public API**.
     * Example snippets if usage changed.
     * **Providers** table if kwargs/env changed.
     * **Common errors** section if relevant.

3. **Examples**

   * Update scripts in `examples/` to reflect current usage.
   * Keep them minimal and runnable.

4. **Docs & README**

   * Ensure README and `docs/index.md` are up-to-date and point to `LLM_READABLE_GUIDE.md`.
   * Update **“## Codebase Structure”** in README with the current folder/file tree.

5. **CHANGELOG.md & DEVLOG.md**

   * Add a brief entry under **Unreleased** in `CHANGELOG.md`.
   * Add design/dev notes in `DEVLOG.md` (optional).

6. **Tests**

   * Update tests if behavior/signatures changed:

     * `tests/test_init_llm.py`
     * `tests/test_monitor_resources.py`
     * `tests/test_llm_readable_guide.py` (ensures all exports are in the guide).

---

### Automated checks (tools/CI do)

7. **Format & Lint (local)**

   ```bash
   black src tests
   ruff check --fix src tests
   ```

   (Windows alt: `.venv/Scripts/black src tests`, `.venv/Scripts/ruff check --fix src tests`)

8. **Run tests (local)**

   ```bash
   pytest -q
   ```

   (Windows alt: `.venv/Scripts/pytest -q`)

9. **Pre-commit hooks**

   * If installed, hooks run automatically on commit.
   * If not installed: `pre-commit install`.

10. **Push & CI**

```bash
git add -A
git commit -m "feat/fix: <summary>"
git push
```

* CI will run lint, format, and tests.
* Fix any issues surfaced in the logs.

---

## 🌱 Submitting Changes

1. Create a new branch:

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Commit your changes (use clear, conventional commit messages):

   ```bash
   git commit -m "feat: add support for remote Anthropic models"
   ```

3. Push your branch:

   ```bash
   git push origin feature/my-new-feature
   ```

4. Open a Pull Request against `main`.

---

## ✅ Code Style

* Python 3.9+
* [Black](https://black.readthedocs.io/) for formatting
* [Ruff](https://docs.astral.sh/ruff/) for linting
* [Mypy](https://mypy-lang.org/) for type checking

These are enforced in CI and via [pre-commit hooks](.pre-commit-config.yaml).

---

## 🧪 Tests

* All code changes must include tests.
* Tests live under the `tests/` directory and use [pytest](https://pytest.org).
* Run with:

  ```bash
  make test
  ```

---

## 💡 Tips

* Look at [DEVLOG.md](DEVLOG.md) for ongoing notes on design decisions.
* See [CHANGELOG.md](CHANGELOG.md) for release history.

---

By following this guide, you’ll help keep **LLMPop** stable, consistent, and chatbot-friendly 🙏