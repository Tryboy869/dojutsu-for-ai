"""
SenjutsuAgent — High-level API (simplest interface).
Wraps PrecisionAbsolutePipeline into a clean result object.
"""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, List

from senjutsu.core.pipeline   import PrecisionAbsolutePipeline
from senjutsu.core.rag_booster import SkillsRAG
from senjutsu.core.security   import SkillSecurityValidator


@dataclass
class AgentResult:
    byakugan:    str
    mode_sage:   str
    jougan:      str
    execution:   str
    skills_used: List[str]
    timing:      Dict[str, float]
    total_seconds: float
    raw: dict = field(default_factory=dict)


class SenjutsuAgent:
    """
    Simplest entry point for Senjutsu Coding Agent.

    Quick start:
        from senjutsu import SenjutsuAgent
        agent = SenjutsuAgent(api_key="gsk_...")
        result = agent.run("Create a FastAPI auth service")
        print(result.execution)
    """

    DEFAULT_MODELS = {
        "groq":   "moonshotai/kimi-k2-instruct",
        "openai": "gpt-4o",
    }

    def __init__(
        self,
        api_key: str,
        provider: str = "groq",
        model: Optional[str] = None,
        rag: Optional[SkillsRAG] = None,
        verbose: bool = False,
    ):
        model = model or self.DEFAULT_MODELS.get(provider, "gpt-4o")
        llm_caller = self._build_caller(api_key, provider, model)

        if rag is None:
            rag = SkillsRAG()
            rag.index_all(verbose=False)

        self.pipeline = PrecisionAbsolutePipeline(
            llm_caller=llm_caller,
            rag=rag,
            verbose=verbose,
        )

    def _build_caller(self, api_key: str, provider: str, model: str):
        if provider == "groq":
            try:
                from groq import Groq
            except ImportError:
                raise ImportError("pip install groq")
            client = Groq(api_key=api_key)
            def caller(system, messages, label="", max_tokens=3000):
                t0 = time.time()
                r = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system}] + messages,
                    max_tokens=max_tokens, temperature=0.35,
                )
                return r.choices[0].message.content, time.time() - t0
            return caller

        elif provider == "openai":
            try:
                from openai import OpenAI
            except ImportError:
                raise ImportError("pip install openai")
            client = OpenAI(api_key=api_key)
            def caller(system, messages, label="", max_tokens=3000):
                t0 = time.time()
                r = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system}] + messages,
                    max_tokens=max_tokens,
                )
                return r.choices[0].message.content, time.time() - t0
            return caller

        raise ValueError(f"Unknown provider: {provider}")

    def run(self, task: str) -> AgentResult:
        raw = self.pipeline.run(task)
        steps = raw.get("steps", {})
        rag_hits = steps.get("skills", {}).get("rag_hits", [])
        skills_used = [name for _, name, _ in rag_hits]

        timing = {
            "byakugan":  steps.get("byakugan",  {}).get("time", 0),
            "mode_sage": steps.get("mode_sage", {}).get("time", 0),
            "jougan":    steps.get("jougan",    {}).get("time", 0),
            "skills":    steps.get("skills",    {}).get("time", 0),
            "execution": steps.get("execution", {}).get("time", 0),
        }

        return AgentResult(
            byakugan=steps.get("byakugan",  {}).get("content", ""),
            mode_sage=steps.get("mode_sage",{}).get("content", ""),
            jougan=steps.get("jougan",      {}).get("content", ""),
            execution=steps.get("execution",{}).get("content", ""),
            skills_used=skills_used,
            timing=timing,
            total_seconds=raw.get("total_time", 0),
            raw=raw,
        )
