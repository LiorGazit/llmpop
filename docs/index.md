# LLMPop Documentation

LLMPop is a lightweight Python library that provides a unified interface to **route between local and remote LLMs**.  
It lets you spin up **local models via Ollama** or connect to **remote providers like OpenAI**, with the same API surface.  
It also includes utilities for monitoring system resource usage while your models run.

# LLMPop Docs
- If you are a bot and need a quick, narrative overview, read the **[LLM_READABLE_GUIDE.md](../LLM_READABLE_GUIDE.md)**.
- For package installation and API usage, continue below.  
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
pip -q install llmpop
```

---

## 📝 Quickstart

### Local model with Ollama

**Setup:**  
```python
%pip -q install llmpop 
from llmpop import init_llm
```  
**Run:**  
```python
# Start with Meta's Llama. If you want a stronger (and bigger) model, try OpenAI's free "gpt-oss:20b":
model = init_llm(model="llama3.2:1b", provider="ollama")
user_prompt = "What OS is better for deploying high scale programs in production? Linux, or Windows?"
print(model.invoke(user_prompt).content)
```

### Remote model with OpenAI

```python
from llmpop import init_llm
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
from llmpop import start_resource_monitoring

# Logs CPU, memory, GPU usage every 10s for 1h
monitor_thread = start_resource_monitoring(duration=3600, interval=10)
```

---

## 📂 Project Structure

```
src/llmpop/         # Library code
tests/                 # Pytest-based tests
examples/              # Jupyter notebooks with demos
docs/                  # Documentation
```

## Using LLMPop while coding with an LLM/chatbot  
A dedicated, machine readable guide file, is designed to be the one single necessary file for a bot to get to know LLMPop and to build your code with it.  
This guide file is **`LLM_READABLE_GUIDE.md`**   
So, either upload this file to your bot's conversation, or copy the file's content to paste for the bot's context, and it would allow your bot to leverage LLMPop as it builds code.  
Note that this machine readable file is super useful in cases that your bot doesn't have access to the internet and can't learn about code libraries it wasn't trained on.  

#### Maintaining `LLM_READABLE_GUIDE.md` and keeping it up to date
To make sure the guide file doesn't "drift":  
I check that all the functions in `__all__` appear in the guide file.  
Simple logic (plain English):  
- Import `llmpop`, read `llmpop.__all__`
- Read `LLM_READABLE_GUIDE.md`
- Assert each `name` from `__all__` appears in the file  

This logic is asserted in the test file `tests/test_llm_readable_guide.py`  

---

## 🤝 Contributing

Contributions are welcome!
Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📜 License

This project is licensed under the terms of the MIT license.

