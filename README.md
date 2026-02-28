<div align="center">

![Header](assets/header.svg)

![Logo](assets/logo-eyes.svg)

</div>

---

# 🥷 Senjutsu Coding Agent

**Precision Absolute** — An AI coding agent that doesn't just generate code.  
It *understands* what you actually need before writing a single line.

> *"A vague task becomes production-ready code through structural vision, systemic coherence, and trajectory anticipation."*

---

## How It Works

Senjutsu runs a **5-step analytical pipeline** before generating any code:

| Step | Name | What it does |
|------|------|--------------|
| 1 | **Byakugan** 白眼 | Structural vision — reveals what is *really* needed vs what is said |
| 2 | **Mode Sage** | Systemic coherence — evaluates global consistency, detects architectural drift |
| 3 | **Jōgan** 淨眼 | Trajectory anticipation — spots non-return points, hidden failure modes |
| 4 | **RAG Booster** | Selects the most relevant skills from the registry (TF-IDF scoring) |
| 5 | **Execution** | Generates complete, production-ready code guided by the triple analysis |

The gap between "what you asked" and "what you need" is what Byakugan closes.  
The gap between "what was analyzed" and "what gets coded" is what the pipeline closes.

---

## Installation — Clone & Run

No pip install. No package manager. Just clone and use.

```bash
# 1. Clone the repo
git clone https://github.com/Tryboy869/senjutsu-coding-agent.git
cd senjutsu-coding-agent

# 2. Install the only dependency (Groq SDK)
pip install groq

# 3. Set your API key
export GROQ_API_KEY=gsk_your_key_here

# 4. Run directly
python providers/senjutsu-agent/main.py run "Build a FastAPI auth service with JWT"
```

That's it.

---

## Usage — Allpath Runner (recommended for multi-language projects)

Senjutsu is packaged as an **Allpath Runner** provider — a universal interface that lets any language call it.

### Start the Allpath daemon

```bash
# Download the daemon (if not already in your project)
curl -O https://raw.githubusercontent.com/Tryboy869/allpath-runner/main/allpath-runner.py

# Start it (scans ./providers/ automatically)
python allpath-runner.py daemon &
```

### Call from Python

```python
import socket, json

def senjutsu(function, args=[]):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(120)  # pipeline takes 60-90s
    s.connect('/tmp/allpath_runner.sock')
    s.sendall(json.dumps({
        "package": "senjutsu-agent",
        "function": function,
        "args": args
    }).encode())
    chunks = []
    while chunk := s.recv(65536):
        chunks.append(chunk)
    s.close()
    return json.loads(b''.join(chunks))

# Full pipeline
result = senjutsu("run", ["Build an async job queue with FastAPI", "gsk_xxx"])
print(result["execution"])   # production-ready code
print(result["skills_used"]) # which skills RAG selected

# Quick structural analysis only (1 LLM call)
result = senjutsu("byakugan", ["Build a distributed cache", "gsk_xxx"])
print(result["byakugan"])
```

### Call from JavaScript (Node.js)

```javascript
const net = require('net');

function senjutsu(fn, args = []) {
    return new Promise((resolve, reject) => {
        const client = net.createConnection('/tmp/allpath_runner.sock');
        let data = '';
        client.setTimeout(120000); // 2 min
        client.on('connect', () => client.write(JSON.stringify({
            package: 'senjutsu-agent', function: fn, args
        })));
        client.on('data', chunk => data += chunk);
        client.on('end', () => resolve(JSON.parse(data)));
        client.on('error', reject);
    });
}

const result = await senjutsu('run', ['Build a Redis-backed job queue', 'gsk_xxx']);
console.log(result.execution);
```

### Available functions

| Function | Description | Time |
|----------|-------------|------|
| `run` | Full 5-step pipeline → complete code | ~60-90s |
| `byakugan` | Structural analysis only | ~8-12s |
| `skills_list` | List all indexed RAG skills | instant |
| `skills_count` | Number of indexed skills | instant |
| `check_skill` | Security-validate a skill content | instant |
| `version` | Package version | instant |

---

## Built-in Skills

Senjutsu ships with 6 built-in skills that guide code generation.  
Skills are selected automatically by TF-IDF relevance — not by arbitrary priority.

### `dev-expert`
*Trigger: any code generation task*

Forces the agent to think like an accomplished full-stack developer **before** writing any code.  
Covers: stack selection criteria (maintainability > domain fit > performance > scale), architecture by scale (monolith < 10k users, microservices only when justified), security non-negotiables (input validation, secrets in env, rate limiting), SEO when applicable.

Forbidden patterns it enforces against: hardcoded secrets, SELECT * without LIMIT, "security later" mindset, framework choices driven by trend.

### `async-systems`
*Trigger: job queues, background workers, task processing, producer-consumer*

Non-negotiable patterns for async production systems: bounded queues (`asyncio.Queue(maxsize=N)` — never unbounded), backpressure (block producer when full, return HTTP 503), dead letter queue (failed jobs moved to DLQ, never silently discarded), idempotency keys (check before processing), dual timeouts (soft + hard), worker heartbeats (detect zombie workers).

Stack guidance: asyncio.Queue for < 100 jobs/s, Redis Streams for < 10k/s, Celery + RabbitMQ for high throughput. Always PostgreSQL for job state persistence (Redis is ephemeral).

### `api-security`
*Trigger: any API endpoint, authentication system, web service*

OWASP Top 10 enforcement: Pydantic input validation with field constraints and size limits, rate limiting on every public endpoint (slowapi), JWT signature + expiry verification, secrets via pydantic-settings (app fails to start if missing), CORS with explicit origins list (never `*` in production), security headers (X-Content-Type-Options, X-Frame-Options).

Forbidden: `allow_origins=["*"]`, secrets in code or git, logging request bodies (PII risk), SQL string concatenation.

### `python-backend`
*Trigger: any Python backend project*

2025 production standards: structlog for structured logging (never `print()`), FastAPI lifespan context manager (not deprecated `@app.on_event`), SQLAlchemy 2.0 async sessions, domain exceptions (not raw HTTP codes in business logic), type hints on all functions, project structure with `api/`, `domain/`, `infrastructure/` separation.

Forbidden: `print()` in production, `@app.on_event` (deprecated since FastAPI 0.93), sync `Session` instead of `AsyncSession`, bare `except Exception` without logging.

### `github-actions`
*Trigger: CI/CD workflows, PyPI publishing, Docker builds*

Standard CI/CD template: matrix strategy across Python versions, pytest with coverage gate, mypy type checking, PyPI publish on tag push using OIDC (no stored secrets), pinned action versions (@v4 not @main), concurrency groups to cancel superseded runs.

Anti-patterns: `echo $SECRET` in run steps, unpinned `@main` actions, no timeout, push triggers on every commit.

### `svg-animations`
*Trigger: animated logo, SVG badge, README animation, animated icon*

Professional SVG animation patterns: SMIL animations for morphing and motion paths (impossible in CSS alone), blinking eye pattern with `<animate attributeName="ry">`, gradient color cycling, glow filter with `feGaussianBlur` + `feMerge`, pulse rings with synchronized r and opacity animations.

Performance rules: file size < 50KB (< 20KB for README badges), transform/opacity for GPU acceleration, no external fonts. Accessibility mandatory: `role="img"`, `aria-labelledby`, `prefers-reduced-motion` media query.

*Note: this skill is in the registry for projects that need animated visuals — it does not get selected for backend coding tasks (TF-IDF prevents it).*

---

## Connecting a Skills Registry

Senjutsu's RAG engine can pull additional skills from any public GitHub registry.

```python
from senjutsu.core.rag_booster import SkillsRAG

rag = SkillsRAG()

# Pull from regenrek/agent-skills (verified public registry)
rag.pull_repos(verbose=True)

# Index all skills (built-in + pulled)
rag.index_all(verbose=True)

print(f"{rag.count} skills indexed")
```

Default remote registry: `github.com/regenrek/agent-skills`  
Skills are cached in `.senjutsu_cache/index.json` — indexing only runs once.

---

## Supported LLM Providers

| Provider | Default model | Env var |
|----------|--------------|---------|
| `groq` | `moonshotai/kimi-k2-instruct-0905` | `GROQ_API_KEY` |
| `openai` | `gpt-4o` | `OPENAI_API_KEY` |

---

<div align="center">

![Footer](assets/footer.svg)

</div>
