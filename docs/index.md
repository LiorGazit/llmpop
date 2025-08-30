# LLMRouter Documentation

LLMRouter is a lightweight Python library that provides a unified interface to **route between local and remote LLMs**.  
It lets you spin up **local models via Ollama** or connect to **remote providers like OpenAI**, with the same API surface.  
It also includes utilities for monitoring system resource usage while your models run.

---

## 🚀 Features

- **Local LLMs**: Run models on your machine with [Ollama](https://ollama.ai/).
- **Remote LLMs**: Connect to cloud providers (OpenAI supported out of the box, easily extensible).
- **Unified interface**: Same API regardless of local or remote.
- **Resource monitoring**: Log CPU, memory, and GPU utilization in real time.
- **LangChain integration**: Use with LangChain chains, prompts, and agents directly.

---

## 📦 Installation

### From GitHub (latest):

```bash
pip install git+https://github.com/LiorGazit/LLMRouter.git
```

---

## 📝 Quickstart

### Local model with Ollama

```python
from llmrouter import init_llm

model = init_llm(chosen_llm="gemma3", local_or_remote="local")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")

print((prompt | model).invoke({"q": "What is an agent?"}))
```

### Remote model with OpenAI

```python
from llmrouter import init_llm
import os

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_llm(
    chosen_llm="gpt-4o",
    local_or_remote="remote",
    provider="openai",
    api_key=os.environ["OPENAI_API_KEY"]
)
```

---

## 📊 Resource Monitoring

```python
from llmrouter import start_resource_monitoring

# Logs CPU, memory, GPU usage every 10s for 1h
monitor_thread = start_resource_monitoring(duration=3600, interval=10)
```

---

## 📂 Project Structure

```
src/llmrouter/         # Library code
tests/                 # Pytest-based tests
examples/              # Jupyter notebooks with demos
docs/                  # Documentation
```

---

## 🤝 Contributing

Contributions are welcome!
Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the terms of the MIT license.

