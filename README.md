<div align="center">

![Header](assets/header.svg)

</div>

<div align="center">

![Logo Eyes](assets/logo-eyes.svg)

</div>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-a78bfa?style=flat-square&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-38bdf8?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Allpath Runner](https://img.shields.io/badge/Allpath_Runner-compatible-10b981?style=flat-square&logo=fastapi&logoColor=white)](https://allpath-runner.dev)
[![Skills](https://img.shields.io/badge/RAG_Skills-593%2B-fbbf24?style=flat-square&logo=bookstack&logoColor=white)](senjutsu/skills/)
[![Providers](https://img.shields.io/badge/AI_Providers-6-c084fc?style=flat-square&logo=openai&logoColor=white)](#compatible-with-any-ai-provider)
[![Languages](https://img.shields.io/badge/Client_Examples-8_langs-0ea5e9?style=flat-square&logo=code&logoColor=white)](examples/)
[![Release](https://img.shields.io/github/v/release/Tryboy869/dojutsu-for-ai?style=flat-square&color=10b981&logo=github&label=Release)](https://github.com/Tryboy869/dojutsu-for-ai/releases)
[![Stars](https://img.shields.io/github/stars/Tryboy869/dojutsu-for-ai?style=flat-square&color=fbbf24&logo=github)](https://github.com/Tryboy869/dojutsu-for-ai/stargazers)

</div>

---

# 🥷 Dojutsu-for-AI

**Precision Absolute** — An AI coding agent that thinks before it codes.

> *"A vague task becomes production-ready code through structural vision, systemic coherence, and trajectory anticipation."*

<div align="center">

![Dev Card](assets/dev-card.svg)

</div>

---

## How It Works

Dojutsu-for-AI runs a **5-step analytical pipeline** before generating any code:

| Step | Eye Technique | What it does |
|------|--------------|--------------|
| 1 | **Byakugan** 白眼 | Structural vision — sees what is *really* needed vs what is said |
| 2 | **Mode Sage** | Systemic coherence — detects architectural drift before it happens |
| 3 | **Jōgan** 淨眼 | Trajectory anticipation — spots hidden failure modes and non-return points |
| 4 | **RAG Booster** | Selects the most relevant skills (TF-IDF scoring, 593+ skills indexed) |
| 5 | **Execution** | Generates complete, production-ready code guided by the triple analysis |

---

## Benchmark Results

<div align="center">

![Benchmark](assets/benchmark.svg)

</div>

> **Dojutsu 90% vs Baseline 55%** — The pipeline takes ~10× longer but anticipates
> 8 production failure modes not mentioned in the prompt, and ships with tests + ops scripts.
> See [`tests/benchmarks/`](tests/benchmarks/) for full analysis.

---

## Compatible with Any AI Provider

Dojutsu-for-AI works with **any LLM provider** — proprietary or open source:

| Provider | Example models | Env var |
|----------|---------------|---------|
| **Groq** | `moonshotai/kimi-k2-instruct-0905`, `llama-3.3-70b` | `GROQ_API_KEY` |
| **OpenAI** | `gpt-4o`, `gpt-4o-mini`, `o3` | `OPENAI_API_KEY` |
| **Anthropic** | `claude-opus-4-5`, `claude-sonnet-4-5` | `ANTHROPIC_API_KEY` |
| **Mistral** | `mistral-large-latest`, `codestral-latest` | `MISTRAL_API_KEY` |
| **OpenRouter** | Any model via unified API | `OPENROUTER_API_KEY` |
| **HuggingFace** | `mistralai/Mistral-7B`, `Qwen/Qwen2.5-Coder` | `HUGGINGFACE_API_KEY` |

---

## Quick Start — Clone & Run

No pip install. No package manager. Just clone and use.

```bash
# 1. Clone
git clone https://github.com/Tryboy869/dojutsu-for-ai
cd dojutsu-for-ai

# 2. Install the only runtime dependency
pip install groq  # or: pip install openai / anthropic / mistralai

# 3. Set your API key
export GROQ_API_KEY=gsk_your_key_here
# or: export OPENAI_API_KEY=sk-...
# or: export ANTHROPIC_API_KEY=sk-ant-...

# 4. Run
python providers/dojutsu-agent/main.py run "Build a FastAPI auth service with JWT"
```

---

## Allpath Runner (recommended for multi-language projects)

Dojutsu-for-AI is distributed as an **Allpath Runner** provider — call it from any language.

```bash
# 1. Clone (if not already done)
git clone https://github.com/Tryboy869/dojutsu-for-ai
cd dojutsu-for-ai

# 2. Start the daemon (scans ./providers/ automatically)
python allpath-runner.py daemon &
```

### Call from Python

```python
import socket, json

def dojutsu(fn, args=[]):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(120)
    s.connect('/tmp/allpath_runner.sock')
    s.sendall(json.dumps({"package": "dojutsu-agent", "function": fn, "args": args}).encode())
    chunks = []
    while chunk := s.recv(65536):
        chunks.append(chunk)
    s.close()
    return json.loads(b''.join(chunks))

# Full pipeline — Groq / Kimi
result = dojutsu("run", ["Build an async job queue", "gsk_xxx", "groq"])

# With OpenAI
result = dojutsu("run", ["Build an async job queue", "sk-xxx", "openai", "gpt-4o"])

# With Anthropic
result = dojutsu("run", ["Build an async job queue", "sk-ant-xxx", "anthropic"])

print(result["execution"])    # production-ready code
print(result["skills_used"])  # RAG skills selected
```

### Call from JavaScript

```javascript
const net = require('net');

function dojutsu(fn, args = []) {
    return new Promise((resolve, reject) => {
        const client = net.createConnection('/tmp/allpath_runner.sock');
        let data = '';
        client.setTimeout(120000);
        client.on('connect', () => client.write(JSON.stringify({
            package: 'dojutsu-agent', function: fn, args
        })));
        client.on('data',  chunk => data += chunk);
        client.on('end',   () => resolve(JSON.parse(data)));
        client.on('error', reject);
    });
}

const result = await dojutsu('run', ['Build a Redis cache layer', 'gsk_xxx', 'groq']);
console.log(result.execution);
```

---

## Multi-language Examples

All languages connect to the same Allpath daemon via Unix socket — **zero extra setup**.

<details>
<summary><b>TypeScript / Node.js</b></summary>

```typescript
import * as net from "net";

function dojutsu(fn: string, args: string[] = []): Promise<any> {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection("/tmp/allpath_runner.sock");
    const chunks: Buffer[] = [];
    socket.on("connect", () =>
      socket.write(JSON.stringify({ package: "dojutsu-agent", function: fn, args }))
    );
    socket.on("data",  c => chunks.push(c));
    socket.on("end",   () => resolve(JSON.parse(Buffer.concat(chunks).toString())));
    socket.on("error", reject);
  });
}

const result = await dojutsu("run", [
  "Build a rate limiter with Redis sliding window",
  process.env.GROQ_API_KEY!,
  "groq"
]);
console.log(result.execution);
```

</details>

<details>
<summary><b>Go</b></summary>

```go
func dojutsu(fn string, args []string) (*DojutsuResult, error) {
    conn, _ := net.DialTimeout("unix", "/tmp/allpath_runner.sock", 5*time.Second)
    defer conn.Close()
    req, _ := json.Marshal(map[string]any{
        "package": "dojutsu-agent", "function": fn, "args": args,
    })
    conn.Write(req)
    data, _ := io.ReadAll(conn)
    var result DojutsuResult
    json.Unmarshal(data, &result)
    return &result, nil
}

result, _ := dojutsu("run", []string{
    "Build a Go HTTP middleware for JWT auth",
    os.Getenv("GROQ_API_KEY"), "groq",
})
fmt.Println(result.Execution)
```

</details>

<details>
<summary><b>Rust</b></summary>

```rust
async fn dojutsu(function: &str, args: Vec<&str>) -> anyhow::Result<DojutsuResult> {
    let mut stream = UnixStream::connect("/tmp/allpath_runner.sock").await?;
    let payload = serde_json::to_vec(&Request { package: "dojutsu-agent", function, args })?;
    stream.write_all(&payload).await?;
    stream.shutdown().await?;
    let mut buf = Vec::new();
    stream.read_to_end(&mut buf).await?;
    Ok(serde_json::from_slice(&buf)?)
}

let result = dojutsu("run", vec![
    "Build an Axum REST API with PostgreSQL pool",
    &api_key, "groq",
]).await?;
println!("{}", result.execution.unwrap_or_default());
```

</details>

<details>
<summary><b>Java</b></summary>

```java
JSONObject result = DojutsuClient.call(
    "run",
    "Build a Spring Boot API with JWT auth and Redis caching",
    System.getenv("GROQ_API_KEY"),
    "groq"
);
System.out.println(result.getString("execution"));
```

Full client → [`examples/DojutsuClient.java`](https://github.com/Tryboy869/dojutsu-for-ai/blob/main/examples/DojutsuClient.java)

</details>

<details>
<summary><b>PHP</b></summary>

```php
$result = dojutsu('run', [
    'Build a Laravel 11 API with Sanctum auth and Horizon',
    getenv('GROQ_API_KEY'), 'groq',
]);
echo $result['execution'];
```

Full client → [`examples/client.php`](https://github.com/Tryboy869/dojutsu-for-ai/blob/main/examples/client.php)

</details>

<details>
<summary><b>Ruby</b></summary>

```ruby
result = dojutsu("run", [
  "Build a Rails 8 API with Devise JWT and Sidekiq",
  ENV["GROQ_API_KEY"], "groq"
])
puts result["execution"]
```

Full client → [`examples/client.rb`](https://github.com/Tryboy869/dojutsu-for-ai/blob/main/examples/client.rb)

</details>

<details>
<summary><b>C# / .NET 8</b></summary>

```csharp
var result = await Dojutsu.CallAsync(
    "run",
    "Build an ASP.NET Core 8 API with EF Core and Hangfire",
    Environment.GetEnvironmentVariable("GROQ_API_KEY")!,
    "groq"
);
Console.WriteLine(result.Execution);
```

Full client → [`examples/DojutsuClient.cs`](https://github.com/Tryboy869/dojutsu-for-ai/blob/main/examples/DojutsuClient.cs)

</details>

> All provider params (`groq`, `openai`, `anthropic`, `mistral`, `openrouter`, `huggingface`) work identically across every language.
> Complete runnable files in [`examples/`](https://github.com/Tryboy869/dojutsu-for-ai/tree/main/examples).

---

## Available Functions

| Function | Description | Time |
|----------|-------------|------|
| `run` | Full 5-step pipeline → complete code | ~60-90s |
| `byakugan` | Structural analysis only (1 LLM call) | ~8-12s |
| `skills_list` | List all 593+ indexed skills | instant |
| `skills_count` | Number of indexed skills | instant |
| `check_skill` | Security-validate a skill file | instant |
| `version` | Package version + supported providers | instant |

---

## SVG Assets

The `assets/` folder contains **5 animated SVGs** built for this README:

| File | Content | Used for |
|------|---------|---------|
| `header.svg` | Animated title with scanning line + particle effects | Top of README |
| `logo-eyes.svg` | Blinking Byakugan × Jōgan eyes (blink + eye-tracking) | Identity / hero |
| `dev-card.svg` | Creator card with animated border + floating particles | Author section |
| `footer.svg` | Gradient footer with traveling light dot | Bottom of README |
| `benchmark.svg` | Cinematic Baseline vs Dojutsu comparison | Benchmark section |

All animations respect `prefers-reduced-motion` for accessibility.

---

<div align="center">

![Footer](assets/footer.svg)

</div>
