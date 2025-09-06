# LLM-Router
The Python library that lets you spin up any LLM with a single function.  

### Devs: [Lior Gazit](https://github.com/LiorGazit), and GPT5  
*Hours spent in total on this project so far: `13 hours`  

## Features
- Plug-and-play local LLMs via Ollama—no cloud or API costs required.  
- Easy remote API support (OpenAI, extendable).  
- Unified interface: Seamlessly switch between local and remote models in your code.  
- Resource monitoring: Track CPU, memory, and (optionally) GPU usage while your agents run.  

## Using LLM-Router while coding with an LLM/chatbot  
A dedicated, machine readable guide file, is designed to be the one single necessary file for a bot to get to know LLM-Router and to build your code with it.  
This guide file is **`LLM_READABLE_GUIDE.md`**   
So, either upload this file to your bot's conversation, or copy the file's content to paste for the bot's context, and it would allow your bot to leverage LLM-Router as it builds code.  
Note that this machine readable file is super useful in cases that your bot doesn't have access to the internet and can't learn about code libraries it wasn't trained on.  
More on this guide file in `docs/index.md`  

## Quick start via Colab
Start by running `run_ollama_in_colab.ipynb` in [Colab](https://colab.research.google.com/github/LiorGazit/llm_router/blob/main/examples/run_ollama_in_colab.ipynb).  

## Codebase Structure  
llm_router/  
├─ .github/  
│  └─ workflows/  
│     └─ ci.yml  
├─ docs/  
│  └─ index.md  
├─ examples/  
│  ├─ quickstart_local.ipynb  
│  └─ quickstart_remote_openai.ipynb  
├─ src/  
│  └─ llm_router/  
│     ├─ __init__.py  
│     ├─ version.py  
│     ├─ init_llm.py  
│     └─ monitor_resources.py  
├─ tests/  
│  ├─ test_init_llm.py  
│  ├─ test_llm_readable_guide.py  
│  └─ test_monitor_resources.py  
├─ .gitignore  
├─ .pre-commit-config.yaml  
├─ CHANGELOG.md  
├─ CODE_OF_CONDUCT.md  
├─ CONTRIBUTING.md  
├─ DEVLOG.md  
├─ LICENSE  
├─ LLM_READABLE_GUIDE.md   
├─ Makefile            
├─ pyproject.toml  
├─ README.md  
├─ requirements-dev.txt      
└─ requirements.txt   

Where:  
• `src/` layout is the modern standard for packaging.  
• `tests/` use pytest; we’ll mock shell/network so CI doesn’t try to actually install/run Ollama.  
• `examples/` contains notebooks users can run locally/Colab.  
• `docs/` is optional now; you can add mkdocs later.  
• `CI` runs lint + unit tests on pushes and PRs.  
• `CHANGELOG` follows Keep a Changelog; DEVLOG is your running engineering journal.  

## Quick setting up  
1. Install from GitHub    
`pip install git+https://github.com/LiorGazit/llm_router.git`  

2. Try it  
    ```python
    from llm_router import init_llm, start_resource_monitoring
    from langchain_core.prompts import ChatPromptTemplate

    model = init_llm(model="gemma3", provider="ollama")
    # Or:
    # os.environ["OPENAI_API_KEY"] = "sk-..."
    # model = init_llm(chosen_llm="gpt-4o", provider="openai")

    prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
    print((prompt | model).invoke({"q":"What is an agent?"}).content)
    ```

 3. Optional - Resource Monitoring
    ```python
    monitor_thread = start_resource_monitoring(duration=600, interval=10)
    ```

Enjoy!