"""
🥷 Senjutsu Coding Agent — Allpath Runner Provider
Entry point: python main.py <function> [args...]
stdout = résultat JSON  |  stderr = erreur + exit(1)
"""
import sys
import json
import os
import subprocess

# ── Auto-install senjutsu si absent ─────────────────────────────────────────
try:
    import senjutsu  # noqa: F401
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "senjutsu"])


HELP = {
    "run":          "run <task> <api_key> [provider=groq] [model] [verbose=false]",
    "byakugan":     "byakugan <task> <api_key> [provider=groq] [model]",
    "skills_list":  "skills_list",
    "skills_count": "skills_count",
    "check_skill":  "check_skill <content>",
    "version":      "version",
}


def run(task: str, api_key: str = "", provider: str = "groq",
        model: str = "", verbose: str = "false") -> None:
    """Pipeline complet Précision Absolue — 5 étapes LLM."""
    key = api_key or os.environ.get("GROQ_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        _err("API key required. Pass as arg or set GROQ_API_KEY env var.")

    from senjutsu import SenjutsuAgent
    from senjutsu.core.rag_booster import SkillsRAG

    rag = SkillsRAG()
    rag.index_all(verbose=False)
    agent = SenjutsuAgent(
        api_key=key, provider=provider,
        model=model or None, rag=rag,
        verbose=(verbose.lower() == "true"),
    )
    result = agent.run(task)
    print(json.dumps({
        "byakugan":    result.byakugan,
        "mode_sage":   result.mode_sage,
        "jougan":      result.jougan,
        "execution":   result.execution,
        "skills_used": result.skills_used,
        "timing":      result.timing,
        "total_time":  result.total_seconds,
    }, ensure_ascii=False))


def byakugan(task: str, api_key: str = "", provider: str = "groq", model: str = "") -> None:
    """Analyse structurelle seule — 1 appel LLM."""
    key = api_key or os.environ.get("GROQ_API_KEY", "")
    if not key:
        _err("API key required.")
    from senjutsu import SenjutsuAgent
    from senjutsu.core.byakugan import Byakugan
    _defaults = {"groq": "moonshotai/kimi-k2-instruct-0905", "openai": "gpt-4o"}
    _agent = SenjutsuAgent.__new__(SenjutsuAgent)
    llm = _agent._build_caller(key, provider, model or _defaults.get(provider, "moonshotai/kimi-k2-instruct-0905"))
    result = Byakugan(llm).analyze(task)
    print(json.dumps({"byakugan": result["content"], "time": result["time"]}, ensure_ascii=False))


def skills_list() -> None:
    from senjutsu.core.rag_booster import SkillsRAG
    rag = SkillsRAG(); rag.index_all(verbose=False)
    print(rag.list_skills())


def skills_count() -> None:
    from senjutsu.core.rag_booster import SkillsRAG
    rag = SkillsRAG(); rag.index_all(verbose=False)
    print(json.dumps({"count": rag.count}))


def check_skill(skill_content: str) -> None:
    from senjutsu.core.security import is_skill_safe
    is_safe, violations = is_skill_safe(skill_content)
    print(json.dumps({"safe": is_safe, "violations": violations}))


def version() -> None:
    import senjutsu
    print(json.dumps({"version": senjutsu.__version__}))


def _err(msg: str):
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


DISPATCH = {
    "run": run, "byakugan": byakugan,
    "skills_list": skills_list, "skills_count": skills_count,
    "check_skill": check_skill, "version": version,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Function name required",
            "available": list(DISPATCH.keys()),
            "usage": {k: f"python main.py {v}" for k, v in HELP.items()},
        }), file=sys.stderr)
        sys.exit(1)
    fn = sys.argv[1]
    if fn not in DISPATCH:
        _err(f"Unknown function '{fn}'. Available: {list(DISPATCH.keys())}")
    try:
        DISPATCH[fn](*sys.argv[2:])
    except TypeError as e:
        _err(f"Wrong arguments for '{fn}': {e}. Usage: python main.py {HELP.get(fn, fn)}")
    except Exception as e:
        _err(str(e))
