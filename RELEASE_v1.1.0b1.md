# 🥷 Senjutsu Coding Agent — v1.1.0b1

**Release date:** 2026-02-28  
**Type:** Beta patch  
**Distribution:** Clone & run — no pip install required

---

## What changed

### Bugs fixed

**RAG scoring** — The previous version had arbitrary `+500` bonus points hardcoded for three skills (`dev-expert`, `github-actions`, `svg-animations`). This caused `svg-animations` to appear in results for any task regardless of relevance — including backend job queue requests. Replaced with real TF-IDF scoring: `score = name_match(3×idf) + desc_match(2×idf) + body_match(idf×log-tf)`. Skills now rank purely by relevance.

**Remote repos** — `anthropics/skills`, `microsoft/skills`, `vercel-labs/skills` were listed as skill sources but don't exist as public repos. `pull_repos()` was silently failing. Replaced with verified public repos: `regenrek/agent-skills`, `PatrickJS/awesome-cursorrules`.

**Pipeline gap** — Byakugan correctly identified critical patterns (dead letter queue, race conditions, idempotency) but the execution step wasn't forcing these into the generated code. Added `_extract_pitfalls()` which injects Byakugan-identified risks directly into the execution prompt as mandatory implementation points.

### Added

**Persistent cache** — Skills index is saved to `.senjutsu_cache/index.json` after first run. Subsequent starts load instantly instead of re-scanning everything.

**`retrieve_for_execution()`** — RAG retrieval now enriches the query with Byakugan/Jōgan analysis content, improving skill recall for the actual implementation needs vs surface-level keywords.

**3 new built-in skills:** `async-systems`, `api-security`, `python-backend` — covering the most common production scenarios that were previously missing.

**Allpath Runner distribution** — Senjutsu is now a first-class Allpath provider. Clone the repo, point Allpath daemon at `providers/senjutsu-agent/`, call from any language.

### Changed

**Footer SVG** — Updated version display from `v1.0.0-beta` to `v1.1.0-beta`, replaced `pip install senjutsu` with `git clone → allpath-runner.py daemon` to reflect the new distribution model.

**README** — Full rewrite documenting Allpath consumption pattern, all 6 built-in skills with their trigger conditions and forbidden patterns, registry connection, provider function reference.

---

## How to update

If you already have the repo cloned:

```bash
git pull origin main
```

If cloning fresh:

```bash
git clone https://github.com/Tryboy869/senjutsu-coding-agent.git
cd senjutsu-coding-agent
pip install groq
export GROQ_API_KEY=gsk_your_key
python providers/senjutsu-agent/main.py run "your task here"
```

---

## Files changed in this patch

```
providers/senjutsu-agent/main.py          # entry point (auto-installs senjutsu)
providers/senjutsu-agent/allpath.expose.json  # manifest (version bump)
senjutsu/skills/async_systems/SKILL.md    # new
senjutsu/skills/api_security/SKILL.md     # new
senjutsu/skills/python_backend/SKILL.md   # new
assets/footer.svg                         # version + distribution text updated
README.md                                 # full rewrite
```

Core modules (`rag_booster.py`, `pipeline.py`) are part of the `senjutsu` package installed separately via pip. The fixes in these modules will be published to PyPI as `senjutsu==1.1.0b1` separately.
