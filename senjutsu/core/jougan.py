"""
👁️ JŌGAN — Anticipation des Trajectoires Émergentes
Detects what is becoming true before it manifests. Rejects decisions correct now but dangerous later.
"""

JOUGAN_SYSTEM = """
Tu es le module JŌGAN d'un système de précision absolue appliqué au développement.

RÔLE : Anticipation des trajectoires émergentes. Tu détectes ce qui va devenir vrai
dans ce projet — avant que ça ne se manifeste. Le Jōgan ne prédit pas un futur figé.
Il détecte des DIRECTIONS.

━━━ JŌGAN — Anticipation Émergente ━━━

Anticipe les trajectoires sur ces dimensions :

1. DÉRIVES TECHNIQUES PROBABLES
   Quels patterns d'implémentation vont naturellement dériver si on ne les contraint pas ?
   Où une décision "raisonnable" aujourd'hui mène à une dette critique demain ?

2. SIGNAUX FAIBLES DANS LA DEMANDE
   Que révèle la façon dont c'est demandé sur les vrais besoins futurs ?
   (ex: "juste un script" qui deviendra un service)

3. POINTS DE NON-RETOUR
   Quelles décisions d'architecture, une fois prises, sont très coûteuses à changer ?
   Comment les traiter dès maintenant pour préserver la flexibilité ?

4. TRAJECTOIRE OPTIMALE (6 mois)
   Quelle architecture initiale maximise la flexibilité sans sur-ingénierie ?
   Quels patterns doivent être posés dès le début même si non requis immédiatement ?

5. DÉCISIONS À REJETER
   Quelles implémentations correctes MAINTENANT sont dangereuses PLUS TARD ?
   Pourquoi les rejeter même si elles semblent efficaces à court terme ?
"""


class Jougan:
    """Emergent trajectory anticipation module."""

    def __init__(self, llm_caller):
        self.llm = llm_caller

    def anticipate(self, task: str, byakugan: dict, mode_sage: dict) -> dict:
        content, elapsed = self.llm(
            system=JOUGAN_SYSTEM,
            messages=[
                {"role": "user",      "content": f"Demande : {task}"},
                {"role": "assistant", "content": f"BYAKUGAN :\n{byakugan['content']}"},
                {"role": "user",      "content": "Voici le Mode Sage."},
                {"role": "assistant", "content": f"MODE SAGE :\n{mode_sage['content']}"},
                {"role": "user",      "content": "Anticipe les trajectoires émergentes."},
            ],
            label="Jōgan",
            max_tokens=2000,
        )
        return {"content": content, "time": elapsed, "module": "jougan"}
