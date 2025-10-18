# Dev Log
## [Unreleased]
- Added Colab demo UI notebook (Gradio front end). Intention: showcase LLMPop without bundling UI into library.
- Packaging tightened: ensure notebooks/examples are not in sdist; wheel unaffected (src-only).
- Docs pass: README “Quick Guides,” updated folder tree; docs index points to human-readable guide.
- The UI notebook `multi_llm_webapp.ipynb` now streams the LLM responses in real time.   
- The UI notebook now checks for the case the the user picked a remote LLM but did not insert an API key.  
- - `multi_llm_webapp.ipynb` now has no unnecessary output. Just prints out the url for opening the UI and that's it.  

## [0.2.3] – 2025-09-12
- Updated `pyproject.toml` classifiers to restrict OS support (Linux + MacOS only).
- Ensured `README.md` is properly linked in metadata for PyPI page rendering.
- Prepped release bump to 0.2.3.

### 2025-09-08 - Examples upgrade  
- Updating the simple example to spin up Llama instead of the open source GPT, for a quicker run.  

### 2025-09-07 — Project Rename to LLMPop
- Published **llmpop 0.2.2** to PyPI.
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