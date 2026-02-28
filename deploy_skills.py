#!/usr/bin/env python3
# Patch skills v1.1.1 — ajoute 20 skills builtins dans le repo
# 1. Colle tes tokens, 2. Upload dans Colab, 3. Run All, 4. Upload le ZIP

GITHUB_TOKEN    = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
GITHUB_USERNAME = "Tryboy869"
REPO_NAME       = "senjutsu-coding-agent"
COMMIT_MSG      = "feat: add 20 built-in skills (react, typescript, docker, postgres, llm-api, ...)"
TAG             = "v1.1.1-skills"

_missing = [k for k, v in {"GITHUB_TOKEN": GITHUB_TOKEN}.items() if "XXXX" in v]
if _missing:
    raise Exception(f"Tokens manquants : {_missing}")

import subprocess, sys, shutil, zipfile
from pathlib import Path

def pip(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"'{cmd}' failed:\n{r.stderr[:400]}")
    return r.stdout.strip()

pip("rich")
from rich.console import Console
from rich.table   import Table
console = Console()

# ── Upload ZIP ─────────────────────────────────────────────────
from google.colab import files as _cf
console.print("[cyan]📁 Upload du ZIP des skills...[/cyan]")
uploaded = _cf.upload()
zip_name = list(uploaded.keys())[0]
zip_dest = Path("/tmp/skills_patch.zip")

for c in [Path("/content")/zip_name,
          *sorted(Path("/content").glob("*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)]:
    if c.exists() and c.stat().st_size > 1000:
        shutil.copy2(str(c), str(zip_dest))
        try:
            with zipfile.ZipFile(str(zip_dest)) as z: z.namelist()
            break
        except: pass

with zipfile.ZipFile(str(zip_dest)) as z:
    entries = z.namelist()
console.print(f"[green]✅ ZIP valide — {len(entries)} fichiers[/green]")

# ── Clone ───────────────────────────────────────────────────────
WORK = Path("/tmp/skills_deploy")
if WORK.exists(): shutil.rmtree(WORK)
WORK.mkdir()
REPO = WORK / "repo"
EXTRACT = WORK / "patch"
EXTRACT.mkdir()

clone_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
r = subprocess.run(["git","clone","--depth=1",clone_url,str(REPO)], capture_output=True, text=True)
if r.returncode != 0:
    raise RuntimeError(r.stderr[:300])
console.print("[green]✅ Repo cloné[/green]")

# ── Patch ───────────────────────────────────────────────────────
with zipfile.ZipFile(str(zip_dest)) as z:
    z.extractall(str(EXTRACT))

zip_root = EXTRACT
for item in EXTRACT.iterdir():
    if item.is_dir(): zip_root = item; break

patched = []
for src in zip_root.rglob("*"):
    if src.is_file():
        rel = src.relative_to(zip_root)
        dst = REPO / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        patched.append(str(rel))

console.print(f"[green]✅ {len(patched)} fichiers ajoutés[/green]")

# Compter les skills dans le repo
skills = [d for d in (REPO/"senjutsu"/"skills").iterdir() if d.is_dir()]
console.print(f"[bold]📚 Total skills dans le repo : {len(skills)}[/bold]")

table = Table(title="Skills builtins")
table.add_column("Skill", style="cyan")
for s in sorted(skills):
    table.add_row(s.name)
console.print(table)

# ── Push ────────────────────────────────────────────────────────
sh('git config user.email "anzize.contact@proton.me"', cwd=str(REPO))
sh('git config user.name "Daouda Abdoul Anzize"', cwd=str(REPO))
sh("git add -A", cwd=str(REPO))
sh(f'git commit -m "{COMMIT_MSG}"', cwd=str(REPO))
remote = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
sh("git remote remove origin", cwd=str(REPO))
sh(f"git remote add origin {remote}", cwd=str(REPO))
sh("git push -u origin main --force", cwd=str(REPO))

# Tag
sh(f"git tag {TAG}", cwd=str(REPO))
sh(f"git push origin {TAG}", cwd=str(REPO))

console.print(f"\n[bold green]🎉 {len(skills)} skills pushés → github.com/{GITHUB_USERNAME}/{REPO_NAME}[/bold green]")
console.print(f"[cyan]Tag : {TAG}[/cyan]")
console.print("\n[dim]Pour tester :[/dim]")
console.print(f"  git clone https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
console.print(f"  python providers/senjutsu-agent/main.py skills_count")
