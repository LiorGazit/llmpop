# init_llm.py

import os
import platform
import shutil
import subprocess
import sys
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


def _command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def _is_linux() -> bool:
    return sys.platform.startswith("linux")


def _is_windows() -> bool:
    return sys.platform.startswith("win")


def _get_linux_distro_id() -> str:
    try:
        return platform.freedesktop_os_release().get("ID", "").lower()
    except Exception:
        return ""


def _ollama_cli_env(host: str, port: int) -> Dict[str, str]:
    env = os.environ.copy()
    env["OLLAMA_HOST"] = f"{host}:{port}"
    return env


def _ollama_model_exists(model: str, host: str, port: int) -> bool:
    res = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        env=_ollama_cli_env(host, port),
    )
    if res.returncode != 0:
        raise RuntimeError(f"Error listing Ollama models: {res.stderr}")

    installed_models = set()
    for line in res.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("name "):
            continue
        installed_models.add(stripped.split()[0])

    return model in installed_models or f"{model}:latest" in installed_models


def _missing_ollama_deps():
    if not _is_linux():
        return []

    missing = []
    if not _command_exists("zstd"):
        missing.append("zstd")
    if not _command_exists("lspci"):
        missing.append("pciutils")
    return missing


def install_ollama_deps(*, verbose: bool = True):
    if not _is_linux():
        raise RuntimeError("Ollama system dependencies are only supported on Linux.")

    missing = _missing_ollama_deps()
    if not missing:
        if verbose:
            print("Ollama system dependencies already installed.")
        return

    distro_id = _get_linux_distro_id()
    sudo = []
    if hasattr(os, "geteuid") and os.geteuid() != 0 and _command_exists("sudo"):
        sudo = ["sudo"]

    if "ubuntu" in distro_id or "debian" in distro_id:
        cmds = [
            sudo + ["apt-get", "update"],
            sudo + ["apt-get", "install", "-y", "zstd", "pciutils"],
        ]
    elif "fedora" in distro_id or "rhel" in distro_id or "centos" in distro_id:
        cmds = [sudo + ["dnf", "install", "-y", "zstd", "pciutils"]]
    elif "arch" in distro_id:
        cmds = [sudo + ["pacman", "-S", "--noconfirm", "zstd", "pciutils"]]
    else:
        deps_str = ", ".join(missing)
        raise RuntimeError(
            "Missing system dependencies for Ollama: "
            f"{deps_str}. Unsupported distro '{distro_id or 'unknown'}'. "
            "Install zstd and pciutils with your package manager."
        )

    if verbose:
        deps_str = ", ".join(missing)
        print(f"Installing system dependencies for Ollama: {deps_str}")
    for cmd in cmds:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            deps_str = ", ".join(missing)
            raise RuntimeError(
                f"Error installing system dependencies ({deps_str}): {res.stderr}"
            )


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
    Create and return a LangChain ChatModel for the given provider.

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
                "host": "127.0.0.1",   # default
                "port": 11434,         # default
                "auto_install": True,  # default
                "auto_serve": True,    # default
                "pull": True           # default; skips when model already exists
              }
          - provider="openai":
              {
                "api_key": "...",  # else taken from OPENAI_API_KEY env var
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
    - Returns a ChatModel so downstream `chain.invoke(...)` consistently yields an AIMessage.
    """
    provider = (provider or "").strip().lower()
    provider_kwargs = dict(provider_kwargs or {})

    if provider == "ollama":
        if _is_windows():
            raise RuntimeError(
                "Ollama is not supported on Windows. Use Linux/macOS or choose "
                "a remote LLM provider (e.g., OpenAI)."
            )

        # Extract provider settings with sensible defaults
        host = provider_kwargs.get("host", "127.0.0.1")
        port = int(provider_kwargs.get("port", 11434))
        auto_install = bool(provider_kwargs.get("auto_install", True))
        auto_serve = bool(provider_kwargs.get("auto_serve", True))
        do_pull = bool(provider_kwargs.get("pull", True))
        missing_deps = _missing_ollama_deps()
        if missing_deps:
            deps_str = ", ".join(missing_deps)
            raise RuntimeError(
                "Missing system dependencies for Ollama: "
                f"{deps_str}. Run llmpop.install_ollama_deps() first, or install "
                "zstd and pciutils with your package manager."
            )

        # 1) Ensure Ollama binary exists (if requested)
        if shutil.which("ollama") is None:
            if auto_install:
                if verbose:
                    print("Installing Ollama...")
                install = subprocess.run(
                    "curl -fsSL https://ollama.com/install.sh | sh",
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
                print("Starting Ollama server...")
            serve_cmd = f"OLLAMA_HOST={host}:{port} ollama serve > serve.log 2>&1 &"
            proc = subprocess.Popen(
                serve_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
            )
            if verbose:
                print(f"Ollama PID: {proc.pid}")

            # 3) Wait until it is ready
            if verbose:
                print("Waiting for Ollama to be ready...")
            wait_for_ollama_ready(host=host, port=port)
            if verbose:
                print("Ready!\n")

        # 4) Pull the requested model only when it is not already installed
        if do_pull:
            if _ollama_model_exists(model, host, port):
                if verbose:
                    print(f"Model '{model}' is already available locally. Skipping pull.")
            else:
                if verbose:
                    print(f"Pulling model '{model}'...")
                pull = subprocess.run(
                    ["ollama", "pull", model],
                    capture_output=True,
                    text=True,
                    env=_ollama_cli_env(host, port),
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
            print("Setting up remote OpenAI chat model...")

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
