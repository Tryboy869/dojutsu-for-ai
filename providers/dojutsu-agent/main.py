"""
🥷 Dojutsu-for-AI — Allpath Runner Provider
Entry point: python main.py <function> [args...]

Compatible providers: groq | openai | huggingface | openrouter | anthropic | mistral
stdout = JSON result  |  stderr = error + exit(1)
"""
import sys, json, os, subprocess

# Auto-install senjutsu if missing
try:
    import senjutsu
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "senjutsu"])

PROVIDER_DEFAULTS = {
    "groq":        "moonshotai/kimi-k2-instruct-0905",
    "openai":      "gpt-4o",
    "anthropic":   "claude-sonnet-4-5",
    "mistral":     "mistral-large-latest",
    "openrouter":  "openai/gpt-4o",
    "huggingface": "mistralai/Mistral-7B-Instruct-v0.3",
}

PROVIDER_ENV = {
    "groq":        "GROQ_API_KEY",
    "openai":      "OPENAI_API_KEY",
    "anthropic":   "ANTHROPIC_API_KEY",
    "mistral":     "MISTRAL_API_KEY",
    "openrouter":  "OPENROUTER_API_KEY",
    "huggingface": "HUGGINGFACE_API_KEY",
}

def _get_key(api_key, provider):
    if api_key and "XXXX" not in api_key:
        return api_key
    env_var = PROVIDER_ENV.get(provider, "GROQ_API_KEY")
    key = os.environ.get(env_var, "")
    if not key:
        _err(f"API key required. Pass as arg or set {env_var} env var.")
    return key

def _err(msg):
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)

def run(task, api_key="", provider="groq", model="", verbose="false"):
    """Full 5-step Precision Absolute pipeline."""
    from senjutsu import SenjutsuAgent
    from senjutsu.core.rag_booster import SkillsRAG
    key = _get_key(api_key, provider)
    rag = SkillsRAG(); rag.index_all(verbose=False)
    agent = SenjutsuAgent(api_key=key, provider=provider,
                          model=model or None, rag=rag,
                          verbose=(verbose.lower() == "true"))
    result = agent.run(task)
    print(json.dumps({
        "byakugan": result.byakugan, "mode_sage": result.mode_sage,
        "jougan": result.jougan, "execution": result.execution,
        "skills_used": result.skills_used, "timing": result.timing,
        "total_time": result.total_seconds,
    }, ensure_ascii=False))

def byakugan(task, api_key="", provider="groq", model=""):
    """Structural analysis only — 1 LLM call."""
    from senjutsu.core.byakugan import Byakugan
    from senjutsu import SenjutsuAgent
    key = _get_key(api_key, provider)
    _m = model or PROVIDER_DEFAULTS.get(provider, "moonshotai/kimi-k2-instruct-0905")
    agent = SenjutsuAgent.__new__(SenjutsuAgent)
    llm = agent._build_caller(key, provider, _m)
    result = Byakugan(llm).analyze(task)
    print(json.dumps({"byakugan": result["content"], "time": result["time"]}, ensure_ascii=False))

def skills_list():
    from senjutsu.core.rag_booster import SkillsRAG
    rag = SkillsRAG(); rag.index_all(verbose=False)
    print(rag.list_skills())

def skills_count():
    from senjutsu.core.rag_booster import SkillsRAG
    rag = SkillsRAG(); rag.index_all(verbose=False)
    print(json.dumps({"count": rag.count}))

def check_skill(skill_content):
    from senjutsu.core.security import is_skill_safe
    safe, v = is_skill_safe(skill_content)
    print(json.dumps({"safe": safe, "violations": v}))

def version():
    import senjutsu
    print(json.dumps({"version": getattr(senjutsu, "__version__", "2.0.0"),
                      "package": "dojutsu-for-ai",
                      "providers": list(PROVIDER_DEFAULTS.keys())}))

DISPATCH = {"run": run, "byakugan": byakugan, "skills_list": skills_list,
            "skills_count": skills_count, "check_skill": check_skill, "version": version}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"available": list(DISPATCH.keys()),
                          "usage": "python main.py <function> [args...]",
                          "providers": list(PROVIDER_DEFAULTS.keys())}), file=sys.stderr)
        sys.exit(1)
    fn = sys.argv[1]
    if fn not in DISPATCH:
        _err(f"Unknown function '{fn}'. Available: {list(DISPATCH.keys())}")
    try:
        DISPATCH[fn](*sys.argv[2:])
    except TypeError as e:
        _err(f"Wrong args for '{fn}': {e}")
    except Exception as e:
        _err(str(e))
