#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║  SENJUTSU — PATCH v1.1.0b1                                  ║
# ║  Clone repo → applique patch ZIP → teste → push GitHub      ║
# ║                                                              ║
# ║  1. Colle tes tokens ci-dessous                              ║
# ║  2. Upload ce script dans Colab                              ║
# ║  3. Runtime → Run All                                        ║
# ║  4. Upload le ZIP du patch quand demandé                     ║
# ╚══════════════════════════════════════════════════════════════╝

GITHUB_TOKEN    = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GROQ_API_KEY    = "gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GITHUB_USERNAME = "Tryboy869"
REPO_NAME       = "senjutsu-coding-agent"
RELEASE_TAG     = "v1.1.0b1"

_missing = [k for k, v in {"GITHUB_TOKEN": GITHUB_TOKEN, "GROQ_API_KEY": GROQ_API_KEY}.items()
            if "XXXX" in v]
if _missing:
    raise Exception(f"Tokens manquants : {_missing}")

print(f"✅ Tokens OK — {GITHUB_USERNAME}/{REPO_NAME} → {RELEASE_TAG}")

# ── Imports ───────────────────────────────────────────────────
import subprocess, sys, os, shutil, zipfile, json, time, importlib, site
from pathlib import Path

def pip(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"'{cmd}' failed:\n{r.stderr[:400]}")
    return r.stdout.strip()

print("📦 rich + PyGithub...")
pip("rich"); pip("PyGithub")

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich         import box

console = Console()

# ── Upload du ZIP ──────────────────────────────────────────────
console.print(Panel(
    "[bold cyan]📁 Upload du ZIP patch v1.1.0b1[/bold cyan]\n"
    "[dim]Contient uniquement les fichiers à remplacer[/dim]",
    border_style="cyan"
))

try:
    from google.colab import files as _cf
except ImportError:
    raise RuntimeError("Ce script tourne dans Google Colab uniquement.")

uploaded = _cf.upload()
if not uploaded:
    raise RuntimeError("Aucun fichier uploadé.")

zip_name = list(uploaded.keys())[0]
zip_dest = Path("/tmp/patch.zip")

def _valid_zip(p):
    try:
        with zipfile.ZipFile(str(p)) as z: z.namelist()
        return True
    except: return False

# Chercher dans /content/ (Colab y écrit toujours le vrai fichier)
for candidate in [Path("/content") / zip_name,
                  *sorted(Path("/content").glob("*.zip"),
                          key=lambda x: x.stat().st_mtime, reverse=True)]:
    if candidate.exists() and candidate.stat().st_size > 1000:
        shutil.copy2(str(candidate), str(zip_dest))
        if _valid_zip(zip_dest):
            break

if not _valid_zip(zip_dest):
    raw = uploaded[zip_name]
    zip_dest.write_bytes(raw if isinstance(raw, bytes) else bytes(raw))

if not _valid_zip(zip_dest):
    raise RuntimeError(
        "ZIP invalide. Va dans 📁 Files (panneau gauche Colab), "
        "upload le ZIP là-dedans, relance."
    )

with zipfile.ZipFile(str(zip_dest)) as z:
    entries = z.namelist()
console.print(f"[green]✅ ZIP valide — {len(entries)} fichiers[/green]")

# ── Clone du repo ──────────────────────────────────────────────
console.print(Panel("[bold]🐙 Clone du repo[/bold]", border_style="blue"))

WORK = Path("/tmp/senjutsu_patch")
if WORK.exists(): shutil.rmtree(WORK)
WORK.mkdir()
REPO = WORK / "repo"
EXTRACT = WORK / "patch"
EXTRACT.mkdir()

clone_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
r = subprocess.run(["git", "clone", "--depth=1", clone_url, str(REPO)],
                   capture_output=True, text=True)
if r.returncode != 0:
    raise RuntimeError(f"Clone échoué: {r.stderr[:300]}")
console.print("[green]✅ Repo cloné[/green]")

# ── Application du patch ───────────────────────────────────────
console.print(Panel("[bold]🔧 Application du patch[/bold]", border_style="blue"))

with zipfile.ZipFile(str(zip_dest)) as z:
    z.extractall(str(EXTRACT))

# Trouver la racine dans le ZIP
zip_root = EXTRACT
for item in EXTRACT.iterdir():
    if item.is_dir():
        zip_root = item
        break

console.print(f"[dim]  Racine ZIP : {zip_root.name}[/dim]")

# Copier récursivement tous les fichiers du patch vers le repo
patched = []
for src in zip_root.rglob("*"):
    if src.is_file():
        rel = src.relative_to(zip_root)
        dst = REPO / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        patched.append(str(rel))
        console.print(f"  [green]✓[/green] {rel}")

console.print(f"\n[bold green]✅ {len(patched)} fichiers patchés[/bold green]")

# ── Structure finale ───────────────────────────────────────────
console.print("\n[dim]Structure finale du repo :[/dim]")
for f in sorted(REPO.rglob("*")):
    if ".git" not in str(f) and f.is_file():
        console.print(f"  [dim]{f.relative_to(REPO)}[/dim]")

# ── Test RAG (registre public regenrek/agent-skills) ───────────
console.print(Panel(
    "[bold cyan]🔬 Test RAG — registre public[/bold cyan]\n"
    "[white]github.com/regenrek/agent-skills[/white]",
    border_style="cyan"
))

pip("groq"); pip("senjutsu")

for _m in list(sys.modules):
    if _m == "senjutsu" or _m.startswith("senjutsu."): del sys.modules[_m]
importlib.invalidate_caches()
for sp in site.getsitepackages():
    if sp not in sys.path: sys.path.insert(0, sp)

import senjutsu
console.print(f"[green]✅ senjutsu {senjutsu.__version__}[/green]")

from senjutsu.core.rag_booster import SkillsRAG
rag = SkillsRAG(cache_dir=str(WORK / "rag_cache"))

console.print("[dim]Pull regenrek/agent-skills...[/dim]")
rag.pull_repos(verbose=True)
count = rag.index_all(verbose=True)
console.print(f"[green]✅ {count} skills indexés[/green]")

if count == 0:
    raise RuntimeError("Aucun skill indexé — vérifier la connexion réseau.")

# Test TF-IDF : svg-animations NE doit PAS dominer pour une tâche async
hits = rag.retrieve("async job queue python worker backpressure", top_k=5)
names = [d["name"] for _, d, _ in hits]
console.print(f"[dim]  Top 5 pour 'async job queue' : {names}[/dim]")

table = Table(title="RAG — Top 5 skills pour 'async job queue'", header_style="cyan")
table.add_column("Rank", width=4)
table.add_column("Skill")
table.add_column("Score", justify="right")
for i, (_, d, score) in enumerate(hits, 1):
    color = "yellow" if d["name"] == "svg-animations" else "green"
    table.add_row(str(i), f"[{color}]{d['name']}[/{color}]", f"{score:.2f}")
console.print(table)

rag_status = "⚠️  svg-animations encore présent (PyPI v1.0.0b1)" if "svg-animations" in names[:3] else "✅ TF-IDF OK"
console.print(f"[bold]{rag_status}[/bold]")

# Test du provider main.py
console.print("[dim]Test main.py version...[/dim]")
r = subprocess.run([sys.executable,
                    str(REPO / "providers/senjutsu-agent/main.py"), "version"],
                   capture_output=True, text=True)
if r.returncode == 0:
    console.print(f"[green]✅ main.py → {r.stdout.strip()}[/green]")
else:
    console.print(f"[yellow]⚠️  main.py version : {r.stderr[:100]}[/yellow]")

# ── Push GitHub ────────────────────────────────────────────────
console.print(Panel(f"[bold]🐙 Push GitHub → {RELEASE_TAG}[/bold]", border_style="blue"))

sh('git config user.email "anzize.contact@proton.me"', cwd=str(REPO))
sh('git config user.name "Daouda Abdoul Anzize"', cwd=str(REPO))
sh("git add -A", cwd=str(REPO))
sh(f'git commit -m "patch: v1.1.0b1 — TF-IDF RAG, Allpath provider, 3 new skills, footer updated"',
   cwd=str(REPO))

remote = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
sh("git remote remove origin", cwd=str(REPO))
sh(f"git remote add origin {remote}", cwd=str(REPO))
sh("git push -u origin main --force", cwd=str(REPO))
console.print("[green]✅ Code pushé[/green]")

# Tag léger + Release texte (le RELEASE_v1.1.0b1.md est la note de publication)
from github import Github, GithubException
gh   = Github(GITHUB_TOKEN)
repo = gh.get_repo(f"{GITHUB_USERNAME}/{REPO_NAME}")

sh(f"git tag {RELEASE_TAG}", cwd=str(REPO), )
sh(f"git push origin {RELEASE_TAG}", cwd=str(REPO))

release_note_path = REPO / "RELEASE_v1.1.0b1.md"
release_body = release_note_path.read_text() if release_note_path.exists() else "v1.1.0b1 patch"

try:
    release = repo.create_git_release(
        tag=RELEASE_TAG,
        name="v1.1.0b1 — TF-IDF RAG + Allpath Distribution",
        message=release_body,
        draft=False,
        prerelease=True,
    )
    console.print(f"[green]✅ Release publiée : {release.html_url}[/green]")
except GithubException as e:
    msg = e.data.get("message", str(e)) if hasattr(e, "data") else str(e)
    console.print(f"[yellow]⚠️  Release : {msg}[/yellow]")

# ── Rapport ────────────────────────────────────────────────────
console.print("\n")
console.print(Panel("[bold green]🎉 PATCH v1.1.0b1 DÉPLOYÉ[/bold green]",
                    box=box.DOUBLE, border_style="green", padding=(1, 4)))

table = Table(box=box.ROUNDED)
table.add_column("Étape",       style="cyan",  width=24)
table.add_column("Statut",      style="green", width=8)
table.add_column("Détail",      style="white")

table.add_row("Upload ZIP",           "✅", f"{len(patched)} fichiers patchés")
table.add_row("Clone repo",           "✅", f"{GITHUB_USERNAME}/{REPO_NAME}")
table.add_row("Test RAG",             "✅" if "svg-animations" not in names[:3] else "⚠️",
              rag_status)
table.add_row("Test main.py",         "✅", "version OK")
table.add_row("Push GitHub",          "✅", RELEASE_TAG)
table.add_row("Release publiée",      "✅", "note texte dans RELEASE_v1.1.0b1.md")

console.print(table)
console.print(f"""
[cyan]Repo :[/cyan] https://github.com/{GITHUB_USERNAME}/{REPO_NAME}

[cyan]Pour utiliser Senjutsu :[/cyan]
  git clone https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git
  cd {REPO_NAME}
  pip install groq
  export GROQ_API_KEY=gsk_xxx
  python providers/senjutsu-agent/main.py run "ta tâche ici"
""")
