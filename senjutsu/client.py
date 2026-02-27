"""
🔌 Senjutsu — High-level client + Allpath Runner compatible interface.

Usage (direct Python):
    from senjutsu.client import SenjutsuClient
    client = SenjutsuClient(api_key="gsk_...", provider="groq")
    result = client.run("Build a REST API with FastAPI...")

Usage (Allpath Runner):
    allpath.call("senjutsu-coding-agent", "run", [task, api_key])
"""

import time
from typing import Optional, Tuple

from senjutsu.core.pipeline   import PrecisionAbsolutePipeline
from senjutsu.core.rag_booster import SkillsRAG
from senjutsu.core.security   import SkillSecurityValidator


def _make_groq_caller(api_key: str, model: str):
    try:
        from groq import Groq
    except ImportError:
        raise ImportError("pip install groq")
    client = Groq(api_key=api_key)

    def caller(system: str, messages: list, label: str, max_tokens: int = 3000) -> Tuple[str, float]:
        t0 = time.time()
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=max_tokens,
            temperature=0.35,
        )
        return resp.choices[0].message.content, time.time() - t0

    return caller


def _make_openai_caller(api_key: str, model: str):
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("pip install openai")
    client = OpenAI(api_key=api_key)

    def caller(system: str, messages: list, label: str, max_tokens: int = 3000) -> Tuple[str, float]:
        t0 = time.time()
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content, time.time() - t0

    return caller


class SenjutsuClient:
    """
    Main entry point for Senjutsu Coding Agent.

    Providers supported: groq, openai, anthropic (via openai-compatible)
    """

    DEFAULT_MODELS = {
        "groq":    "moonshotai/kimi-k2-instruct",
        "openai":  "gpt-4o",
    }

    def __init__(
        self,
        api_key: str,
        provider: str = "groq",
        model: Optional[str] = None,
        skills_cache_dir: str = ".senjutsu_cache",
        local_skills_dir: Optional[str] = None,
        verbose: bool = True,
    ):
        self.verbose = verbose
        model = model or self.DEFAULT_MODELS.get(provider, "gpt-4o")

        if provider == "groq":
            llm_caller = _make_groq_caller(api_key, model)
        elif provider == "openai":
            llm_caller = _make_openai_caller(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'groq' or 'openai'.")

        # Security validator with LLM
        validator = SkillSecurityValidator(llm_caller)

        # RAG engine
        self.rag = SkillsRAG(
            cache_dir=skills_cache_dir,
            local_skills_dir=local_skills_dir,
            security_validator=validator,
        )

        # Pipeline
        self.pipeline = PrecisionAbsolutePipeline(
            llm_caller=llm_caller,
            rag=self.rag,
            verbose=verbose,
        )

    def setup(self, pull_remote: bool = True) -> "SenjutsuClient":
        """Pull remote skill repos and index all skills. Call once before run()."""
        if pull_remote:
            if self.verbose:
                print("📦 Pulling skill repositories...")
            self.rag.pull_repos(verbose=self.verbose)
        if self.verbose:
            print("📚 Indexing skills...")
        self.rag.index_all(verbose=self.verbose)
        if self.verbose:
            print(f"✅ {self.rag.count} skills ready\n")
        return self

    def run(self, task: str) -> dict:
        """Run the full Precision Absolue pipeline on a task."""
        return self.pipeline.run(task)

    @property
    def skills_count(self) -> int:
        return self.rag.count
