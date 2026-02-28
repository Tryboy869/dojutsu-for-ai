# Changelog — Dojutsu-for-AI

## [2.2.0] — 2026-02-28

### Fixed
- README.md — réécriture complète : toutes les URLs pointent vers `https://github.com/Tryboy869/dojutsu-for-ai`
- README.fr.md — idem
- Badges pro ajoutés (MIT, Python, Allpath Runner, Skills, Providers, Languages, Release, Stars)
- `benchmark.svg` ajouté dans le tableau SVG Assets (5ème SVG)
- Section "How It Works" repositionnée avant Benchmark Results
- Exemples multilangage — liens directs vers les fichiers dans `examples/`

---

## [2.1.0] — 2026-02-28

### Added
- `assets/benchmark.svg` — animated benchmark visualization (film-style cinematic)
- `examples/` — 8 language clients: TypeScript, Go, Rust, Java, PHP, Ruby, C#, Python
- `tests/benchmarks/001_async_job_queue.md` — full benchmark analysis
- `tests/benchmarks/README.md` — benchmark index
- README sections: benchmark results + multi-language examples (collapsible)
- README.fr.md — section benchmark en français

### Changed
- Repo renamed: `senjutsu-coding-agent` → `dojutsu-for-ai`
- All internal URLs updated to new repo name

---

## [2.0.0] — 2026-02-28

### 🔄 Rebrand complet
- Renamed package: `senjutsu-coding-agent` → `dojutsu-for-ai`
- Renamed provider: `senjutsu-agent` → `dojutsu-agent`
- Distribution: Allpath Runner uniquement (plus de PyPI)

### 🌐 Multi-provider IA
- Support natif: Groq, OpenAI, Anthropic, Mistral, OpenRouter, HuggingFace
- `provider` param accepte n'importe quel endpoint compatible OpenAI
- Auto-détection de la clé API via variables d'environnement

### 📚 Skills
- 593 skills intégrés (harvest automatique depuis 7 repos publics)
- RAG TF-IDF réel (suppression des bonus arbitraires +500)
- Cache persistant `.senjutsu_cache/index.json`

### 🤖 GitHub Actions
- Auto-release déclenché à chaque nouvelle section dans CHANGELOG.md
- Script shell `scripts/detect_release.sh` pour la détection de version
- Aucune dépendance PyPI / aucun build nécessaire

### 🧹 Nettoyage
- Suppression des fichiers de déploiement Colab obsolètes
- Suppression de `pyproject.toml` (plus de package Python à builder)
- README reécrits (EN + FR) avec les 4 SVG animés

---

## [1.0.0b1] — 2026-02-26

### Added
- Initial beta release — Senjutsu Coding Agent
- Byakugan, Mode Sage, Jōgan, RAG Booster, pipeline 5 étapes
- Allpath Runner integration
- 26 skills builtins
- README EN + FR, 4 SVG animés
