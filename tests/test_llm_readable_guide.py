import importlib
import pathlib


def test_public_api_in_guide():
    pkg = importlib.import_module("llmrouter")
    public_api = getattr(pkg, "__all__", [])
    guide_path = pathlib.Path(__file__).resolve().parents[1] / "LLM_READABLE_GUIDE.md"
    guide_text = guide_path.read_text(encoding="utf-8")

    missing = [name for name in public_api if name not in guide_text]
    assert (
        not missing
    ), f"The following exports are missing from LLM_READABLE_GUIDE.md: {missing}"
