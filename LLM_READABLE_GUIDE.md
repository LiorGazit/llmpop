# LLM-Router — One-File Guide (for Chatbots & Humans)

**Purpose:** single file to copy-paste into chatbots.  
**Install:** `pip install git+https://github.com/LiorGazit/llm_router.git`

## Quickstart — Ollama (local)
```python
from llm_router import init_llm
from langchain_core.prompts import ChatPromptTemplate

model = init_llm(model="gemma3", provider="ollama", provider_kwargs={"pull": True}, temperature=0.0, verbose=False)
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
print((prompt | model).invoke({"q": "What comes first, 1 or 2?"}).content)
```

## Quickstart — OpenAI (remote)

```python
from llm_router import init_llm
from langchain_core.prompts import ChatPromptTemplate
import os

os.environ["OPENAI_API_KEY"] = "sk-..."
model = init_llm(model="gpt-4o", provider="openai", temperature=0.0)
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
print((prompt | model).invoke({"q": "What comes first, 1 or 2?"}).content)
```

## Optional: plain string output

```python
from langchain_core.output_parsers import StrOutputParser
chain = prompt | model | StrOutputParser()
print(chain.invoke({"q": "What comes first, 1 or 2?"}))
```

---

## Public API (stable names)

* `init_llm(model: str, provider: str, provider_kwargs: dict | None = None, **chat_init_kwargs) -> ChatModel`
  Returns a LangChain **ChatModel** (ChatOllama / ChatOpenAI) with consistent behavior across providers.

* `start_resource_monitoring(logfile: str = "resource_usage.log", duration: int = 3600, interval: int = 10) -> threading.Thread`
  Starts a daemon thread logging CPU/Mem/GPU usage; returns the thread.

---

## Providers (kwargs & env)

### `ollama`

* `provider_kwargs`:

  * `host: str` (default `127.0.0.1`)
  * `port: int` (default `11434`)
  * `auto_install: bool` (default `True`)
  * `auto_serve: bool` (default `True`)
  * `pull: bool` (default `True`)
* Env: `OLLAMA_HOST` (optional override)
* Notes: Starts server automatically when `auto_serve=True`. Returns ChatOllama.

### `openai`

* `provider_kwargs`:

  * `api_key: str` (optional; otherwise use env)
* Env: `OPENAI_API_KEY` (required if `api_key` not passed)
* Notes: No interactive prompts; returns ChatOpenAI.

---

## Common errors & fixes

* **Missing `OPENAI_API_KEY`** → set env var or pass `provider_kwargs={"api_key": "..."}`
* **Connection refused on `http://127.0.0.1:11434`** → Ollama not serving; keep `auto_serve=True` or run `ollama serve`
* **Model not found in Ollama** → set `pull=True` or `ollama pull <model>`  

## Other Exports
- `__version__` — current package version string.