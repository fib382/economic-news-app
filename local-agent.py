import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_PROVIDER = "ollama"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder:7b"
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash"

PROFILES = {
    "ollama": {
        "speed_patch": {
            "temperature": 0.08,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 8192,
            "num_predict": 768,
        },
        "coding": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 8192,
            "num_predict": 2048,
        },
        "quality_patch": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 8192,
            "num_predict": 3072,
        },
        "test_generation": {
            "temperature": 0.15,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 8192,
            "num_predict": 2048,
        },
        "repair": {
            "temperature": 0.1,
            "top_p": 0.85,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 8192,
            "num_predict": 4096,
        },
        "review": {
            "temperature": 0.1,
            "top_p": 0.85,
            "top_k": 40,
            "repeat_penalty": 1.0,
            "num_ctx": 12288,
            "num_predict": 2048,
        },
    },
    "gemini": {
        "fast_review": {"temperature": 0.2, "top_p": 0.9, "max_output_tokens": 2048},
        "coding_plan": {"temperature": 0.2, "top_p": 0.9, "max_output_tokens": 4096},
        "review": {"temperature": 0.15, "top_p": 0.9, "max_output_tokens": 4096},
        "deep_review": {"temperature": 0.15, "top_p": 0.9, "max_output_tokens": 8192},
        "json": {
            "temperature": 0.1,
            "top_p": 0.85,
            "max_output_tokens": 4096,
            "response_mime_type": "application/json",
        },
    },
}

DENY_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*secret*",
    "*token*",
    "data/*",
    ".tmp/*",
    "*.sqlite",
    "*.db",
    "*.dump",
    "*.sql",
    "*.csv",
    "*.log",
)

SECRET_PATTERNS = (
    re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
    re.compile(r"sk-[0-9A-Za-z_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"https://discord(?:app)?\.com/api/webhooks/[^\s'\"]+"),
)


def strip_code_fence(text: str) -> str:
    stripped = text.strip()
    match = re.fullmatch(r"```[a-zA-Z0-9_-]*\s*\n(?P<body>.*)\n```", stripped, re.DOTALL)
    if match:
        return match.group("body").strip() + "\n"
    return text


def is_denied_path(path: Path) -> bool:
    normalized = path.as_posix()
    names = [normalized, path.name]
    return any(fnmatch.fnmatch(name, pattern) for name in names for pattern in DENY_PATTERNS)


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def get_profile(provider: str, profile: str) -> dict:
    provider_profiles = PROFILES.get(provider)
    if provider_profiles is None:
        raise ValueError(f"Unsupported provider: {provider}")
    if profile not in provider_profiles:
        available = ", ".join(sorted(provider_profiles))
        raise ValueError(f"Unknown profile '{profile}' for {provider}. Available: {available}")
    return provider_profiles[profile]


def build_prompt(instruction: str, content: str, output_mode: str) -> str:
    output_instruction = {
        "full-file": "Return the complete replacement file content only. Do not include Markdown fences or explanations.",
        "diff": "Return a concise unified diff only. Do not include Markdown fences or explanations.",
        "json": "Return valid JSON only. Do not include Markdown fences or explanations.",
        "findings": "Return concise review findings only. Include file/line references when possible.",
    }[output_mode]
    return (
        "Role: focused coding subagent.\n"
        f"Task:\n{instruction}\n\n"
        "Constraints:\n"
        "- Preserve public interfaces unless explicitly instructed.\n"
        "- Use only dependencies already present in the project.\n"
        "- Do not touch unrelated code.\n"
        "- Do not include secrets or environment values.\n\n"
        f"Output:\n{output_instruction}\n\n"
        f"Target file content:\n{content}"
    )


def call_ollama(model: str, prompt: str, options: dict) -> str:
    payload = {"model": model, "prompt": prompt, "stream": False, "options": options}
    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()["response"]


def ensure_google_genai(install_missing_deps: bool) -> None:
    try:
        from google import genai as _genai  # noqa: F401
        from google.genai import types as _types  # noqa: F401
        return
    except ImportError:
        if not install_missing_deps:
            raise RuntimeError(
                "google-genai is not installed. Run: python -m pip install google-genai "
                "or pass --install-missing-deps."
            )

    print("google-genai is missing; installing with current Python environment...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai"])


def call_gemini(model: str, prompt: str, config: dict, install_missing_deps: bool) -> str:
    ensure_google_genai(install_missing_deps)
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set for this process.")

    response_mime_type = config.get("response_mime_type", "text/plain")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=config.get("temperature"),
            top_p=config.get("top_p"),
            max_output_tokens=config.get("max_output_tokens"),
            response_mime_type=response_mime_type,
        ),
    )
    return response.text or ""


def write_or_print(target: Path, text: str, output_mode: str) -> None:
    cleaned = strip_code_fence(text)
    if output_mode == "json":
        json.loads(cleaned)
    if output_mode == "full-file":
        target.write_text(cleaned, encoding="utf-8")
    else:
        print(cleaned)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a focused coding subagent via Ollama or Gemini.")
    parser.add_argument("--provider", choices=("ollama", "gemini"), default=DEFAULT_PROVIDER)
    parser.add_argument("--model")
    parser.add_argument("--profile", default="coding")
    parser.add_argument("--target", required=True)
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--output-mode", choices=("full-file", "diff", "json", "findings"), default="full-file")
    parser.add_argument("--allow-cloud", action="store_true")
    parser.add_argument("--install-missing-deps", action="store_true")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        raise FileNotFoundError(f"Target file does not exist: {target}")
    content = target.read_text(encoding="utf-8")
    model = args.model or (DEFAULT_GEMINI_MODEL if args.provider == "gemini" else DEFAULT_OLLAMA_MODEL)
    profile = get_profile(args.provider, args.profile)

    if args.provider == "gemini":
        if not args.allow_cloud:
            raise RuntimeError("Gemini requires --allow-cloud when sending file contents.")
        if is_denied_path(target):
            raise RuntimeError(f"Refusing to send sensitive path to Gemini: {target}")
        if contains_secret(args.instruction) or contains_secret(content):
            raise RuntimeError("Refusing to send likely secret content to Gemini.")

    prompt = build_prompt(args.instruction, content, args.output_mode)
    print(f"provider={args.provider} model={model} profile={args.profile} target={target.name}")

    if args.provider == "ollama":
        result = call_ollama(model, prompt, profile)
    else:
        result = call_gemini(model, prompt, profile, args.install_missing_deps)

    write_or_print(target, result, args.output_mode)
    print("local-agent complete")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"local-agent error: {exc}", file=sys.stderr)
        sys.exit(1)
