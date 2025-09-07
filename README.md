# LLMPop
The Python library that lets you spin up any LLM with a single function.  
#### Why did we need this library:    
1. Needed a single simple command for any LLM, including the free local LLMs that Ollama offers.  
2. Needed a better way for introducing a code library to a LLM that helps you build code. The `llmpop` library comes with a machine-readable file that is minimal and sufficent, see `LLM_READABLE_GUIDE.md`. 
   Add it to your conversation with the coding LLM and it will learn how to build code with `llmpop`. From a security aspect, this approach is safer then directing your LLM to read someone's entire codebase.  

### Devs: [Lior Gazit](https://github.com/LiorGazit), and GPT5  
Total hours spent in total on this project so far: `17 hours`   

### Quick run of LLMPop:  
Quickest on Colab:  
<a target="_blank" href="https://colab.research.google.com/github/LiorGazit/llmpop/blob/main/examples/quick_run_llmpop.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>  
Or if you want to set it up yourself, pick the free `T4 GPU`, and copy code over:    
```python
print("Installing llmpop:")
%pip -q install llmpop 
print("Done installing llmpop.\n")
from llmpop import init_llm, start_resource_monitoring
from langchain_core.prompts import ChatPromptTemplate

# Spinning up OpenAI's free GPT-OSS-20B, give it a few minutes, it's worth it.
# If you want a quick LLM, set model="llama3.2:1b".
model = init_llm(model="gpt-oss:20b", provider="ollama")
prompt = ChatPromptTemplate.from_template("Q: {q}\nA:")
user_prompt = "What OS is better for deploying high scale programs in production? Linux, or Windows?"
print((prompt | model).invoke({"q":user_prompt}).content)
```

## Features
- Plug-and-play local LLMs via Ollama—no cloud or API costs required.  
- Easy remote API support (OpenAI, extendable).  
- Unified interface: Seamlessly switch between local and remote models in your code.  
- Resource monitoring: Track CPU, memory, and (optionally) GPU usage while your agents run.  

## Using LLMPop while coding with an LLM/chatbot  
A dedicated, machine readable guide file, is designed to be the one single necessary file for a bot to get to know LLMPop and to build your code with it.  
This guide file is **`LLM_READABLE_GUIDE.md`**   
So, either upload this file to your bot's conversation, or copy the file's content to paste for the bot's context, and it would allow your bot to leverage LLMPop as it builds code.  
Note that this machine readable file is super useful in cases that your bot doesn't have access to the internet and can't learn about code libraries it wasn't trained on.  
More on this guide file in `docs/index.md`  

## Quick start via Colab
Start by running `run_ollama_in_colab.ipynb` in [Colab](https://colab.research.google.com/github/LiorGazit/llmpop/blob/main/examples/run_ollama_in_colab.ipynb).  

## Codebase Structure  
llmpop/  
├─ .github/  
│  └─ workflows/  
│     └─ ci.yml  
├─ docs/  
│  └─ index.md  
├─ examples/  
│  ├─ quick_run_llmpop.ipynb  
│  ├─ quick_run_llmpop.py  
│  └─ run_ollama_in_colab.ipynb  
├─ src/  
│  └─ llmpop/  
│     ├─ __init__.py  
│     ├─ init_llm.py   
│     ├─ monitor_resources.py  
│     ├─ py.typed  
│     └─ version.py   
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
`pip -q install llmpop`  

2. Try it  
    ```python
    from llmpop import init_llm, start_resource_monitoring
    from langchain_core.prompts import ChatPromptTemplate

    model = init_llm(model="gemma3:1b", provider="ollama")
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