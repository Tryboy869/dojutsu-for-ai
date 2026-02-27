"""
╔══════════════════════════════════════════════════════════════╗
║  SENJUTSU — Coding Agent with Precision Absolue              ║
║  Byakugan × Mode Sage × Jōgan × RAG Booster × Dev Expert    ║
║  Author  : Daouda Abdoul Anzize  |  Version : 1.0.0-beta     ║
╚══════════════════════════════════════════════════════════════╝
"""
__version__  = "1.0.0b1"
__author__   = "Daouda Abdoul Anzize"
__email__    = "anzize.contact@proton.me"
__license__  = "MIT"

from senjutsu.core.pipeline    import PrecisionAbsolutePipeline
from senjutsu.core.rag_booster import SkillsRAG
from senjutsu.core.security    import SkillSecurityValidator
from senjutsu.agent            import SenjutsuAgent, AgentResult

__all__ = [
    "SenjutsuAgent",
    "AgentResult",
    "PrecisionAbsolutePipeline",
    "SkillsRAG",
    "SkillSecurityValidator",
    "__version__",
]
