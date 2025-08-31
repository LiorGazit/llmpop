# Changelog
All notable changes to this project will be documented here.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [0.2.0] - 2025-08-31
- docs: add LLM_READABLE_GUIDE.md (single-file chatbot guide)
- tests: add tests/test_llm_readable_guide.py to ensure guide stays in sync with __all__
- docs: update README.md and docs/index.md to reference the guide
- docs: expand CONTRIBUTING.md with pre-commit checklist
- docs: update README “Codebase Structure”

## [0.1.0] - 2025-08-30
### Added
- Initial package structure with `init_llm` (local via Ollama, remote via OpenAI).
- `start_resource_monitoring` for CPU/Mem/GPU logging.
- PyPI-ready packaging, tests, CI, pre-commit.
