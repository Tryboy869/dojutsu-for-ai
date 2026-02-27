"""
Senjutsu — Allpath Runner Provider
Exposes Senjutsu pipeline functions via Allpath IPC protocol.
"""
import sys
import json
import os


def run(task: str, api_key: str = "", model: str = "moonshotai/kimi-k2-instruct",
        provider: str = "groq") -> None:
    """Run full Precision Absolute pipeline on a task."""
    key = api_key or os.environ.get("GROQ_API_KEY", "")
    if not key:
        print(json.dumps({"error": "API key required. Pass api_key or set GROQ_API_KEY env var."}))
        return

    from senjutsu import SenjutsuAgent, SkillsRAG
    rag = SkillsRAG()
    rag.index_all()
    agent = SenjutsuAgent(api_key=key, model=model, provider=provider, rag=rag)
    result = agent.run(task)
    print(json.dumps(result.to_dict()))


def byakugan(task: str, api_key: str = "") -> None:
    """Run only Byakugan structural vision on a task."""
    from senjutsu.core.pipeline import SenjutsuPipeline, BYAKUGAN_PROMPT
    key = api_key or os.environ.get("GROQ_API_KEY", "")
    agent = SenjutsuPipeline(api_key=key)
    result, _ = agent._llm(BYAKUGAN_PROMPT, [{"role": "user", "content": f"Request: {task}"}])
    print(json.dumps({"byakugan": result}))


def check_skill(skill_content: str) -> None:
    """Security check a skill's content."""
    from senjutsu.core.pipeline import is_skill_safe
    is_safe, violations = is_skill_safe(skill_content)
    print(json.dumps({"safe": is_safe, "violations": violations}))


def version() -> None:
    """Return package version."""
    import senjutsu
    print(json.dumps({"version": senjutsu.__version__}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Function name required"}), file=sys.stderr)
        sys.exit(1)

    func_name = sys.argv[1]
    args = sys.argv[2:]

    funcs = {"run": run, "byakugan": byakugan, "check_skill": check_skill, "version": version}
    if func_name not in funcs:
        print(json.dumps({"error": f"Unknown function: {func_name}"}), file=sys.stderr)
        sys.exit(1)

    funcs[func_name](*args)
