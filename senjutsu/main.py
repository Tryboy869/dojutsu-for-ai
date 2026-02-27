"""
Allpath Runner entry point.
Called as: python main.py <function_name> [args...]
"""
import sys
import json


def run(task: str, api_key: str, provider: str = "groq", model: str = "") -> None:
    from senjutsu.client import SenjutsuClient
    client = SenjutsuClient(
        api_key=api_key,
        provider=provider,
        model=model or None,
        verbose=False,
    ).setup(pull_remote=False)
    result = client.run(task)
    # Allpath convention: print result to stdout
    print(json.dumps({
        "byakugan":  result["steps"]["byakugan"]["content"],
        "mode_sage": result["steps"]["mode_sage"]["content"],
        "jougan":    result["steps"]["jougan"]["content"],
        "execution": result["steps"]["execution"]["content"],
        "total_time": result["total_time"],
    }, ensure_ascii=False))


def version() -> None:
    from senjutsu import __version__
    print(__version__)


def skills_list() -> None:
    from senjutsu.core.rag_booster import SkillsRAG
    rag = SkillsRAG()
    rag.index_all(verbose=False)
    print(rag.list_skills())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <function> [args...]")
        sys.exit(1)

    fn_name = sys.argv[1]
    args = sys.argv[2:]

    dispatch = {
        "run": lambda: run(*args),
        "version": version,
        "skills_list": skills_list,
    }

    if fn_name not in dispatch:
        print(f"Unknown function: {fn_name}", file=sys.stderr)
        sys.exit(1)

    dispatch[fn_name]()
