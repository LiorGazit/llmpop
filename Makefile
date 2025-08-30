.PHONY: install install-dev fmt lint test build publish clean

# Install runtime requirements (from pyproject.toml)
install:
\tpip install -e .

# Install dev requirements (runtime + requirements-dev.txt)
install-dev: install
\tpip install -r requirements-dev.txt

# Run code formatters
fmt:
\truff check --fix src tests
\tblack src tests

# Run linters without fixing
lint:
\truff check src tests
\tblack --check src tests
\tmypy src

# Run tests
test:
\tpytest -q --disable-warnings --maxfail=1 --cov=llmrouter tests/

# Build distribution
build:
\tpython -m build

# Publish to PyPI (requires twine & credentials set up)
publish:
\ttwine upload dist/*

# Clean build artifacts
clean:
\trm -rf dist build *.egg-info
\tfind . -type d -name "__pycache__" -exec rm -rf {} +
