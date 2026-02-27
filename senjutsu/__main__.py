"""Senjutsu CLI entry point."""
import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="senjutsu",
        description="Senjutsu Coding Agent — Precision Absolute AI Skills Engine"
    )
    parser.add_argument("task", nargs="?", help="Development task to accomplish")
    parser.add_argument("--api-key", default=os.environ.get("GROQ_API_KEY", ""),
                        help="API key (or set GROQ_API_KEY env var)")
    parser.add_argument("--model", default="moonshotai/kimi-k2-instruct")
    parser.add_argument("--provider", default="groq", choices=["groq", "openai"])
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--skills", action="store_true", help="List available skills")

    args = parser.parse_args()

    if args.version:
        import senjutsu
        print(f"senjutsu {senjutsu.__version__}")
        return

    if args.skills:
        from senjutsu.core.pipeline import SkillsRAG
        rag = SkillsRAG(skills_dirs=[])
        rag.index_all()
        print("📚 Available skills:\n")
        print(rag.list_skills())
        return

    if not args.task:
        parser.print_help()
        sys.exit(1)

    if not args.api_key:
        print("❌ API key required. Use --api-key or set GROQ_API_KEY env var.", file=sys.stderr)
        sys.exit(1)

    from senjutsu import SenjutsuAgent, SkillsRAG

    print(f"🥷 Senjutsu — Precision Absolute")
    print(f"📋 Task: {args.task[:80]}...")
    print(f"🤖 Model: {args.model}\n")

    rag = SkillsRAG(skills_dirs=[])
    rag.index_all()
    agent = SenjutsuAgent(api_key=args.api_key, model=args.model,
                          provider=args.provider, rag=rag)

    print("🔵 Byakugan — Structural vision...", end="", flush=True)
    result = agent.run(args.task)
    print(f" ✓ {result.timing.get('byakugan', 0):.1f}s")
    print(f"🌍 Mode Sage ✓ | 👁️  Jōgan ✓ | 📚 RAG ✓")
    print(f"💻 Execution ✓ | Total: {result.total_seconds:.1f}s\n")
    print("=" * 60)
    print("🔵 BYAKUGAN")
    print(result.byakugan)
    print("\n🌍 MODE SAGE")
    print(result.mode_sage)
    print("\n👁️  JŌGAN")
    print(result.jougan)
    print("\n💻 EXECUTION")
    print(result.execution)


if __name__ == "__main__":
    main()
