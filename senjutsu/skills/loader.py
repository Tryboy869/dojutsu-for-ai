"""Loads built-in skills from the package's skills/ directory."""
from pathlib import Path

BUILTIN_SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"

def get_builtin_skill(name: str) -> str:
    path = BUILTIN_SKILLS_DIR / name / "SKILL.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Built-in skill not found: {name}")

def list_builtin_skills():
    return [d.name for d in BUILTIN_SKILLS_DIR.iterdir() if (d / "SKILL.md").exists()]
