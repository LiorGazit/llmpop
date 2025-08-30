# Contributing to LLMRouter

Thanks for your interest in contributing 🎉  
This guide explains how to set up your environment, follow coding standards, and submit pull requests.

---

## 🚀 Getting Started

1. **Fork & clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LLMRouter.git
   cd LLMRouter
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

By following this guide, you’ll help keep **LLMRouter** stable, consistent, and easy to maintain 🙏