"""
📚 RAG BOOSTER — Skills Engine
Gravitational indexing of skills from multiple sources:
- anthropics/skills, microsoft/skills, vercel-labs/skills
- .cursorrules, llms.txt, system prompts
- Local skills (dev-expert, github-actions, svg-animations)
"""

import hashlib
import subprocess
import re
from pathlib import Path
from typing import List, Tuple, Dict, Optional

from senjutsu.core.security import SkillSecurityValidator

# Remote skill sources (cloned on demand)
SKILL_REPOS = {
    "anthropics": "https://github.com/anthropics/skills",
    "microsoft":  "https://github.com/microsoft/skills",
    "vercel":     "https://github.com/vercel-labs/skills",
    "regenrek":   "https://github.com/regenrek/agent-skills",
}

STOPWORDS = {
    "the","a","an","is","to","of","and","or","for","in","on","with","that",
    "this","be","as","at","from","je","le","la","les","un","une","des","et",
    "ou","de","du","pour","sur","si","qui","que","ce","se","il","ils","elle",
    "use","when","skill","file","task","create","make","build","run","add",
}


class SkillsRAG:
    """
    Multi-source skills RAG engine with gravitational scoring.
    Supports: SKILL.md, .cursorrules, llms.txt, YAML agents.
    Built-in security validation on every loaded skill.
    """

    def __init__(
        self,
        cache_dir: str = ".senjutsu_cache",
        local_skills_dir: Optional[str] = None,
        security_validator: Optional[SkillSecurityValidator] = None,
    ):
        self.cache_dir = Path(cache_dir)
        self.local_dir = Path(local_skills_dir) if local_skills_dir else None
        self.validator = security_validator or SkillSecurityValidator()
        self.storage: Dict[str, dict] = {}

    # ── Source acquisition ────────────────────────────────────────────────────

    def pull_repos(self, verbose: bool = True) -> int:
        """Clone or update remote skill repos. Returns number of repos pulled."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        pulled = 0
        for name, url in SKILL_REPOS.items():
            target = self.cache_dir / name
            try:
                if target.exists():
                    subprocess.run(
                        ["git", "-C", str(target), "pull", "--quiet"],
                        capture_output=True, timeout=30
                    )
                else:
                    subprocess.run(
                        ["git", "clone", "--depth=1", "--quiet", url, str(target)],
                        capture_output=True, timeout=60
                    )
                pulled += 1
                if verbose:
                    print(f"  ✓ {name}")
            except Exception as e:
                if verbose:
                    print(f"  ⚠ {name}: {e}")
        return pulled

    # ── Indexing ──────────────────────────────────────────────────────────────

    def index_all(self, verbose: bool = True) -> int:
        """Index all available skill files. Returns total count."""
        sources: List[Path] = []

        # Remote cached repos
        if self.cache_dir.exists():
            sources += list(self.cache_dir.rglob("SKILL.md"))
            sources += list(self.cache_dir.rglob("*.cursorrules"))
            sources += list(self.cache_dir.rglob("llms.txt"))
            sources += list(self.cache_dir.rglob("llms-full.txt"))

        # Local package builtin skills — senjutsu/skills/
        pkg_skills = Path(__file__).parent.parent / "skills"
        if pkg_skills.exists():
            sources += list(pkg_skills.rglob("SKILL.md"))

        # Fallback: root-level skills/ dir (for dev/allpath setups)
        root_skills = Path(__file__).parent.parent.parent / "skills"
        if root_skills.exists() and root_skills != pkg_skills:
            sources += list(root_skills.rglob("SKILL.md"))

        # User-provided local dir
        if self.local_dir and self.local_dir.exists():
            sources += list(self.local_dir.rglob("SKILL.md"))
            sources += list(self.local_dir.rglob("*.cursorrules"))

        loaded = 0
        rejected = 0
        for sf in sources:
            result = self._load_skill_file(sf)
            if result == "ok":
                loaded += 1
            elif result == "rejected":
                rejected += 1

        if verbose:
            print(f"  ✓ {loaded} skills indexed, {rejected} rejected (security)")

        return loaded

    def _load_skill_file(self, path: Path) -> str:
        """Load a single skill file. Returns 'ok', 'rejected', or 'error'."""
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return "error"

        ext  = path.suffix.lower()
        # Raw name from dir/file (replace _ with - for consistency)
        raw_name = (path.parent.name if path.name in ("SKILL.md", "llms.txt", "llms-full.txt")
                    else path.stem).replace("_", "-")
        # Prefer name from SKILL.md frontmatter (e.g. "name: dev-expert")
        name = self._extract_frontmatter_name(raw) or raw_name
        src  = self._detect_source(path)

        # Determine format
        fmt = "skill_md"
        if ext == ".cursorrules":
            fmt = "cursorrules"
        elif path.name.startswith("llms"):
            fmt = "llms_txt"

        desc = self._extract_description(raw, name, fmt)

        # Security validation
        val = self.validator.validate(name, raw)
        if val.get("recommendation") == "reject":
            return "rejected"

        # Use sanitized version if available
        content = val.get("sanitized_version") or raw

        self.storage[f"{src}::{name}"] = {
            "name":    name,
            "source":  src,
            "format":  fmt,
            "description": desc,
            "content": content,
            "path":    str(path),
            "hash":    hashlib.sha256(raw.encode()).hexdigest()[:16],
        }
        return "ok"

    def _detect_source(self, path: Path) -> str:
        p = str(path)
        for name in SKILL_REPOS:
            if name in p:
                return name
        if "skills" in p.lower() and str(Path(__file__).parent) in p:
            return "senjutsu-builtin"
        return "local"

    def _extract_description(self, raw: str, fallback: str, fmt: str) -> str:
        if fmt == "skill_md" and raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 2:
                for line in parts[1].splitlines():
                    if line.strip().startswith("description:"):
                        return line.split(":", 1)[1].strip().strip('"\'')
        # Grab first meaningful line
        for line in raw.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and len(line) > 15:
                return line[:120]
        return fallback

    # ── Retrieval ─────────────────────────────────────────────────────────────

    def _keywords(self, text: str) -> List[str]:
        words = re.findall(r"[a-zA-Z_-]{3,}", text.lower())
        return [w for w in words if w not in STOPWORDS]

    def retrieve(self, query: str, top_k: int = 6) -> List[Tuple[str, dict, int]]:
        """Gravitational scoring retrieval. Returns [(key, data, score)]."""
        words = self._keywords(query)
        scores: Dict[str, int] = {}

        # Pinned builtin skills always included
        pinned = ["dev-expert", "github-actions", "svg-animations"]

        for key, d in self.storage.items():
            name = d["name"].lower()
            desc = (d["description"] or "").lower()
            body = (d["content"][:600]).lower()

            score = 0
            # Pinned bonus
            if any(p in name for p in pinned):
                score += 500

            for w in words:
                if w in name:   score += 15
                if w in desc:   score += 10
                score += body.count(w) * 2

            if score > 0:
                scores[key] = score

        ranked = sorted(scores, key=scores.get, reverse=True)[:top_k]
        return [(k, self.storage[k], scores[k]) for k in ranked if k in self.storage]

    def get_content(self, keys: List[str], max_chars: int = 3000) -> str:
        parts = []
        for key in keys:
            # try direct key or name match
            entry = self.storage.get(key)
            if not entry:
                for k, v in self.storage.items():
                    if v["name"] == key:
                        entry = v
                        break
            if entry:
                sep = "=" * 50
                parts.append(
                    f"\n{sep}\nSKILL [{entry['source']}] : {entry['name']}\n"
                    f"Format: {entry['format']}\n{sep}\n"
                    f"{entry['content'][:max_chars]}"
                )
        return "\n".join(parts)

    def list_skills(self) -> str:
        lines = []
        for key, d in sorted(self.storage.items()):
            src = d["source"]
            fmt = d["format"]
            desc = (d["description"] or "")[:80]
            lines.append(f"• [{d['name']}] ({src}, {fmt}) — {desc}")
        return "\n".join(lines) if lines else "(no skills indexed)"

    @property
    def count(self) -> int:
        return len(self.storage)

    def _extract_frontmatter_name(self, raw: str) -> str:
        """Extract 'name:' field from YAML frontmatter. Returns '' if not found."""
        if not raw.startswith("---"):
            return ""
        parts = raw.split("---", 2)
        if len(parts) < 2:
            return ""
        for line in parts[1].splitlines():
            line = line.strip()
            if line.startswith("name:"):
                return line.split(":", 1)[1].strip().strip('"\'')
        return ""
