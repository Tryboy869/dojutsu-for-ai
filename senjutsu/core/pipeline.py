"""
🌌 PRECISION ABSOLUE PIPELINE
Full orchestration: Byakugan → Mode Sage → Jōgan → RAG → Execution
"""

import time
import json
from typing import Optional, Callable

from senjutsu.core.byakugan   import Byakugan
from senjutsu.core.mode_sage  import ModeSage
from senjutsu.core.jougan     import Jougan
from senjutsu.core.rag_booster import SkillsRAG
from senjutsu.core.security   import SkillSecurityValidator

SKILL_SELECTOR_SYSTEM = """
Tu es un expert en sélection de skills pour agents IA.

Tu reçois l'analyse triple (Byakugan + Mode Sage + Jōgan) d'une tâche,
ainsi que la liste des skills disponibles.

Sélectionne 2-5 skills les plus pertinents.
Les skills "dev-expert", "github-actions" et "svg-animations" sont toujours prioritaires
s'ils sont présents et pertinents.

LISTE DES SKILLS :
{skills_list}

Réponds dans ce format :
SKILLS SÉLECTIONNÉS :
1. [nom] - Raison : ... - Règles critiques : ...
[etc.]

SKILLS ÉCARTÉS :
- [nom] : [raison courte]
"""

EXECUTION_SYSTEM = """
Tu es un développeur full stack expert qui génère du code avec une précision absolue.

Tu as une triple perception du projet :
- BYAKUGAN : la réalité structurelle exacte
- MODE SAGE : la cohérence systémique globale
- JŌGAN : les trajectoires et dérives anticipées

Et des skills précis pour guider l'implémentation.

RÈGLES D'EXÉCUTION :
1. Applique les INTENTIONS des skills, pas juste leurs règles
2. La stack recommandée par Mode Sage EST la stack — pas de déviation
3. Couvre les points de rupture identifiés par Byakugan
4. Pose les fondations que Jōgan a identifiées comme non-retour
5. Sécurité by design — jamais en afterthought
6. Structure de projet complète — code production-ready

FORMAT DE RÉPONSE OBLIGATOIRE :

⚠️ DÉCISIONS DE PRÉCISION ABSOLUE :
[Les 5 décisions clés prises grâce à la triple perception]

📁 STRUCTURE DU PROJET :
[Arborescence complète]

💻 CODE COMPLET :
[Chaque fichier avec son contenu complet]

✅ VALIDATION TRIPLE :
- Byakugan : [le livrable répond-il à la réalité structurelle identifiée ?]
- Mode Sage : [le livrable est-il cohérent globalement ?]
- Jōgan : [le livrable est-il safe pour les trajectoires futures ?]
"""


class PrecisionAbsolutePipeline:
    """
    Full Precision Absolue pipeline.

    Usage:
        from senjutsu import PrecisionAbsolutePipeline
        from senjutsu.core.rag_booster import SkillsRAG

        rag = SkillsRAG()
        rag.pull_repos()
        rag.index_all()

        pipeline = PrecisionAbsolutePipeline(llm_caller=my_caller, rag=rag)
        result = pipeline.run("Build a SaaS analytics dashboard...")
    """

    def __init__(
        self,
        llm_caller: Callable,
        rag: Optional[SkillsRAG] = None,
        verbose: bool = True,
    ):
        self.llm     = llm_caller
        self.rag     = rag or SkillsRAG()
        self.verbose = verbose

        self.byakugan  = Byakugan(llm_caller)
        self.mode_sage = ModeSage(llm_caller)
        self.jougan    = Jougan(llm_caller)
        self.validator = SkillSecurityValidator(llm_caller)

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def run(self, task: str) -> dict:
        t_start = time.time()
        result  = {"task": task, "steps": {}}

        # ── 1. BYAKUGAN ───────────────────────────────────────────────────────
        self._log("🔵 BYAKUGAN — Vision structurelle absolue")
        byakugan = self.byakugan.analyze(task)
        result["steps"]["byakugan"] = byakugan

        # ── 2. MODE SAGE ──────────────────────────────────────────────────────
        self._log("🌍 MODE SAGE — Cohérence systémique globale")
        mode_sage = self.mode_sage.evaluate(task, byakugan)
        result["steps"]["mode_sage"] = mode_sage

        # ── 3. JŌGAN ─────────────────────────────────────────────────────────
        self._log("👁️  JŌGAN — Anticipation des trajectoires")
        jougan = self.jougan.anticipate(task, byakugan, mode_sage)
        result["steps"]["jougan"] = jougan

        # ── 4. RAG — Skills selection ─────────────────────────────────────────
        self._log("📚 RAG BOOSTER — Sélection des skills")
        combined = f"{byakugan['content']}\n{mode_sage['content']}\n{jougan['content']}"
        rag_hits = self.rag.retrieve(combined, top_k=6)

        skills_list = self.rag.list_skills()
        selector_content, t_sel = self.llm(
            system=SKILL_SELECTOR_SYSTEM.format(skills_list=skills_list),
            messages=[
                {"role": "user", "content": f"Demande : {task}"},
                {"role": "assistant", "content": f"ANALYSES :\n{combined[:1500]}"},
                {"role": "user", "content": "Sélectionne les skills précis."},
            ],
            label="Skill selection",
            max_tokens=800,
        )

        top_keys = [k for k, _, _ in rag_hits[:4]]
        skills_content = self.rag.get_content(top_keys)
        result["steps"]["skills"] = {
            "rag_hits": [(k, d["name"], s) for k, d, s in rag_hits],
            "selection": selector_content,
            "time": t_sel,
        }

        # ── 5. EXECUTION ──────────────────────────────────────────────────────
        self._log("💻 EXÉCUTION — Livrable avec précision absolue")
        execution_content, t_exec = self.llm(
            system=EXECUTION_SYSTEM,
            messages=[
                {"role": "user",      "content": f"Demande : {task}"},
                {"role": "assistant", "content": f"BYAKUGAN :\n{byakugan['content']}"},
                {"role": "user",      "content": "Mode Sage + Jōgan analysés."},
                {"role": "assistant", "content": (
                    f"MODE SAGE :\n{mode_sage['content']}\n\n"
                    f"JŌGAN :\n{jougan['content']}"
                )},
                {"role": "user",      "content": "Skills chargés."},
                {"role": "assistant", "content": f"SKILLS :\n{skills_content}"},
                {"role": "user",      "content": "Génère le projet complet avec précision absolue."},
            ],
            label="Final execution",
            max_tokens=4500,
        )
        result["steps"]["execution"] = {"content": execution_content, "time": t_exec}
        result["total_time"] = time.time() - t_start

        self._log(f"✅ Pipeline terminé en {result['total_time']:.1f}s")
        return result

    def to_json(self, result: dict, path: str):
        """Save result to JSON file."""
        serializable = {k: v for k, v in result.items()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
