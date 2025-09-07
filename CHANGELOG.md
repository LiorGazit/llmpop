# Changelog
All notable changes to this project will be documented here.

The format is based on Keep a Changelog and this project adheres to Semantic Versioning.

## [0.2.2] - 2025-09-07
### Changed
- Renamed project/package from `llm_router` → `llmpop`.
  - **PyPI name**: `llmpop`
  - **import name**: `llmpop`
  - **repo name**: `llmpop`
  - **docs branding**: **LLMPop**
- Updated all imports, docs, tests, and guides to reflect the new name.
- Maintained same API (`init_llm`, `start_resource_monitoring`).



## [0.2.1] - 2025-09-05
### Added
- `verbose` flag to `init_llm()` to allow users to minimize output.
  - Default `verbose=True` preserves current behavior.
  - `verbose=False` silences progress messages; only errors are raised.


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
