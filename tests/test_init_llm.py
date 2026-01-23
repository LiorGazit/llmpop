import builtins
import importlib
import types

import pytest

from llmpop.init_llm import init_llm, install_ollama_deps

# Note: Throughout this code, the suffix _mod stand for module:
init_llm_mod = importlib.import_module("llmpop.init_llm")


def test_remote_openai_requires_key(monkeypatch):
    # Ensure no env var leaks into the test
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # No api_key provided via provider_kwargs and no env var -> should raise
    with pytest.raises(ValueError):
        init_llm(
            model="gpt-4o",
            provider="openai",
        )


def test_remote_openai_with_key(monkeypatch):
    # Mock langchain_openai import + class
    fake_mod = types.SimpleNamespace(ChatOpenAI=lambda **kw: ("CHAT_OPENAI", kw))

    def fake_import(name, *args, **kwargs):
        if name == "langchain_openai":
            return fake_mod
        return builtins.__import__(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # Also ensure env var won't interfere
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    model = init_llm(
        model="gpt-4o",
        provider="openai",
        provider_kwargs={"api_key": "test-key"},
        temperature=0.0,
    )
    # Our fake ChatOpenAI returns a tuple ("CHAT_OPENAI", kwargs)
    assert isinstance(model, tuple) and model[0] == "CHAT_OPENAI"
    assert model[1]["model"] == "gpt-4o"
    assert model[1]["api_key"] == "test-key"
    assert model[1]["temperature"] == 0.0


def test_local_ollama_chat_model(monkeypatch):
    # Ensure we don’t actually call curl/ollama
    import subprocess
    import shutil
    import requests

    # Pretend ollama binary exists
    monkeypatch.setattr(shutil, "which", lambda _: "/usr/bin/ollama")

    # Starting server returns a fake process with pid
    monkeypatch.setattr(
        subprocess, "Popen", lambda *a, **k: types.SimpleNamespace(pid=12345)
    )

    # Ollama readiness check succeeds
    monkeypatch.setattr(
        requests, "get", lambda url: types.SimpleNamespace(status_code=200)
    )

    # Any subprocess.run (pull/list/etc.) succeeds
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: types.SimpleNamespace(
            returncode=0, stderr="", stdout="gemma3\n"
        ),
    )

    # Mock langchain_ollama.chat_models import
    fake_mod = types.SimpleNamespace(ChatOllama=lambda **kw: ("CHAT_OLLAMA", kw))
    import builtins as _b

    old_import = _b.__import__

    def fake_import(name, *args, **kwargs):
        if name == "langchain_ollama.chat_models":
            return fake_mod
        return old_import(name, *args, **kwargs)

    monkeypatch.setattr(_b, "__import__", fake_import)

    model = init_llm(model="gemma3", provider="ollama")
    # Our fake ChatOllama returns a tuple ("CHAT_OLLAMA", kwargs)
    assert isinstance(model, tuple) and model[0] == "CHAT_OLLAMA"
    assert model[1]["model"] == "gemma3"
    # The factory passes a base_url to ChatOllama
    assert model[1].get("base_url", "").startswith("http://")


def test_local_ollama_missing_deps_instructions(monkeypatch):
    # Force Linux and missing deps
    monkeypatch.setattr(init_llm_mod, "_is_linux", lambda: True)
    monkeypatch.setattr(init_llm_mod, "_command_exists", lambda _: False)

    with pytest.raises(RuntimeError) as excinfo:
        init_llm(model="gemma3", provider="ollama")

    msg = str(excinfo.value)
    assert "install_ollama_deps" in msg
    assert "zstd" in msg
    assert "pciutils" in msg


def test_install_ollama_deps_runs_package_manager(monkeypatch):
    # Force Linux, missing deps, and Ubuntu
    monkeypatch.setattr(init_llm_mod, "_is_linux", lambda: True)
    monkeypatch.setattr(init_llm_mod, "_command_exists", lambda cmd: cmd == "sudo")
    monkeypatch.setattr(init_llm_mod, "_get_linux_distro_id", lambda: "ubuntu")
    monkeypatch.setattr(init_llm_mod.os, "geteuid", lambda: 0)

    calls = []

    def fake_run(cmd, capture_output=True, text=True):
        calls.append(cmd)
        return types.SimpleNamespace(returncode=0, stderr="", stdout="")

    monkeypatch.setattr(init_llm_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(
        init_llm_mod, "_missing_ollama_deps", lambda: ["zstd", "pciutils"]
    )

    install_ollama_deps(verbose=False)
    assert calls[0] == ["apt-get", "update"]
    assert calls[1] == ["apt-get", "install", "-y", "zstd", "pciutils"]
