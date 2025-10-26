# init_llm.py

import os
import shutil
import subprocess
from time import sleep
from typing import Any, Dict, Optional

import requests


def wait_for_ollama_ready(
    host: str = "127.0.0.1", port: int = 11434, timeout: int = 15
):
    """Poll the Ollama HTTP endpoint until it's up or timeout."""
    url = f"http://{host}:{port}"
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            sleep(1)
    raise RuntimeError(f"Ollama server at {url} failed to start within {timeout}s.")


def _ensure_package(pkg_import: str, pip_name: str, *, verbose: bool = True):
    """Import a package, installing it if missing."""
    try:
        return __import__(pkg_import, fromlist=["*"])
    except ImportError:
        if verbose:
            print(f"Installing {pip_name}...")
        res = subprocess.run(
            f"pip install -U {pip_name}",
            capture_output=True,
            text=True,
            shell=True,
        )
        if res.returncode != 0:
            raise RuntimeError(f"Error installing {pip_name}: {res.stderr}")
        return __import__(pkg_import, fromlist=["*"])


def _resolve_openai_api_key(explicit_key: Optional[str]) -> str:
    """Resolve OpenAI API key with precedence: explicit > env var."""
    if explicit_key:
        return explicit_key
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    raise ValueError(
        "No OpenAI API key provided. Pass it via provider_kwargs['api_key'] "
        "or set the OPENAI_API_KEY environment variable."
    )


def init_llm(
    model: str,
    provider: str,
    provider_kwargs: Optional[Dict[str, Any]] = None,
    verbose: bool = True,
    **chat_init_kwargs: Any,
):
    """
    Create and return a LangChain **ChatModel** for the given provider.

    Parameters
    ----------
    model : str
        The model identifier (e.g., "gemma3", "mistral", "gpt-4o").
    provider : str
        The backend to use, e.g., "ollama", "openai".
    provider_kwargs : dict, optional
        Provider-specific configuration. Examples:
          - provider="ollama":
              {
                "host": "127.0.0.1",  # default
                "port": 11434,        # default
                "auto_install": True, # default
                "auto_serve": True,   # default
                "pull": True          # default
              }
          - provider="openai":
              {
                "api_key": "...",     # else taken from OPENAI_API_KEY env var
              }
    verbose : bool, optional
        If True (default), print progress messages; errors are always raised.
    **chat_init_kwargs :
        Extra kwargs passed to the underlying LangChain ChatModel constructor
        (e.g., temperature=0.0).

    Returns
    -------
    langchain_core.language_models.chat_models.BaseChatModel
        - Ollama: langchain_ollama.chat_models.ChatOllama
        - OpenAI: langchain_openai.ChatOpenAI

    Notes
    -----
    - No interactive prompts are used for credentials. Provide keys via provider_kwargs or env vars.
    - Secrets are never logged.
    - Returns a **ChatModel** so downstream `chain.invoke(...)` consistently yields an AIMessage.
    """
    provider = (provider or "").strip().lower()
    provider_kwargs = dict(provider_kwargs or {})

    if provider == "ollama":
        # Extract provider settings with sensible defaults
        host = provider_kwargs.get("host", "127.0.0.1")
        port = int(provider_kwargs.get("port", 11434))
        auto_install = bool(provider_kwargs.get("auto_install", True))
        auto_serve = bool(provider_kwargs.get("auto_serve", True))
        do_pull = bool(provider_kwargs.get("pull", True))

        # 1) Ensure Ollama binary exists (if requested)
        if shutil.which("ollama") is None:
            if auto_install:
                if verbose:
                    print("🚀 Installing Ollama...")
                install = subprocess.run(
                    "curl https://ollama.ai/install.sh | sh",
                    capture_output=True,
                    text=True,
                    shell=True,
                )
                if install.returncode != 0:
                    raise RuntimeError(f"Error installing Ollama: {install.stderr}")
            else:
                raise RuntimeError(
                    "Ollama not found on PATH and auto_install=False. "
                    "Install Ollama or enable auto_install."
                )

        # 2) Start Ollama serve (if requested)
        if auto_serve:
            if verbose:
                print("🚀 Starting Ollama server...")
            serve_cmd = f"OLLAMA_HOST={host}:{port} ollama serve > serve.log 2>&1 &"
            proc = subprocess.Popen(
                serve_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            if verbose:
                print(f"→ Ollama PID: {proc.pid}")

            # 3) Wait until it’s ready
            if verbose:
                print("⏳ Waiting for Ollama to be ready…")
            wait_for_ollama_ready(host=host, port=port)
            if verbose:
                print("Ready!\n")

        # 4) Pull the requested model (if requested)
        if do_pull:
            if verbose:
                print(f"🚀 Pulling model '{model}'…")
            pull = subprocess.run(
                f"ollama pull {model}",
                capture_output=True,
                text=True,
                shell=True,
            )
            if pull.returncode != 0:
                raise RuntimeError(f"Error pulling '{model}': {pull.stderr}")

        # 5) Ensure ChatOllama is available
        lc_ollama_mod = _ensure_package(
            "langchain_ollama.chat_models", "langchain-ollama"
        )
        ChatOllama = getattr(lc_ollama_mod, "ChatOllama")

        if verbose:
            print("All done setting up Ollama (ChatOllama).\n")
        return ChatOllama(
            model=model, base_url=f"http://{host}:{port}", **chat_init_kwargs
        )

    elif provider == "openai":
        if verbose:
            print("🚀 Setting up remote OpenAI chat model…")

        # Ensure ChatOpenAI is available
        lc_openai_mod = _ensure_package("langchain_openai", "langchain-openai")
        ChatOpenAI = getattr(lc_openai_mod, "ChatOpenAI")

        # Resolve credentials (no prompting; precedence: explicit > env)
        api_key = _resolve_openai_api_key(provider_kwargs.get("api_key"))

        if verbose:
            print("All done setting up OpenAI (ChatOpenAI).\n")
        return ChatOpenAI(model=model, api_key=api_key, **chat_init_kwargs)

    else:
        raise NotImplementedError(
            f"Provider '{provider}' is not supported yet. "
            "Supported providers: 'ollama', 'openai'."
        )
