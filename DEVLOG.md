# Dev Log
### 2025-09-07 — Project Rename to LLMPop
- Changed distribution and import name from `llm_router` → `llmpop`.
- Motivation: PyPI conflict (`llm-router` already taken) and desire for a distinctive, memorable brand.
- Branding conventions:
  - **PyPI / pip**: `llmpop`
  - **Python import**: `llmpop`
  - **Repo**: `llmpop`
  - **Docs branding**: **LLMPop**
- Provided guidance to update README, docs, examples, and tests.
- Considered adding a temporary shim for `llm_router` → decided optional; can be added later if needed for backward compatibility.

## 2025-09-05 — Verbosity control in init_llm
- Introduced a `verbose: bool = True` parameter to `init_llm()`.
- Goal: simplify user experience by reducing unnecessary output when desired.
- Approach: kept **exceptions mandatory**, all other progress/status messages gated by `verbose`.
- Replaced unconditional `print()` calls with `if verbose: print(...)`.
- `_ensure_package()` updated to also respect `verbose` flag.
- Decided **not** to implement full `logging` integration to avoid complexity.
  - Rationale: library is designed for lightweight, notebook-friendly use.
  - Logging may be revisited if the project grows in scope or adoption.

## 2025-08-30
- Set up src layout, tests with mocks, CI pipeline, and optional dependencies.
- Added examples notebooks for quickstart.