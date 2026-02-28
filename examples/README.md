# Dojutsu-for-AI — Multi-language Examples

All examples connect to the **Allpath Runner** daemon via Unix socket.
Same experience, any language.

## Prerequisites (once)

```bash
git clone https://github.com/Tryboy869/dojutsu-for-ai
cd dojutsu-for-ai
python allpath-runner.py daemon &   # start the daemon
```

## Examples

| Language | File | Run |
|----------|------|-----|
| **Python** | `providers/dojutsu-agent/main.py` | `python main.py run "task" $GROQ_API_KEY groq` |
| **TypeScript** | `examples/typescript.ts` | `npx ts-node examples/typescript.ts` |
| **Go** | `examples/go.go` | `go run examples/go.go` |
| **Rust** | `examples/rust.rs` | `cargo run` |
| **Java** | `examples/DojutsuClient.java` | `javac -cp json.jar DojutsuClient.java && java DojutsuClient` |
| **PHP** | `examples/client.php` | `php examples/client.php` |
| **Ruby** | `examples/client.rb` | `ruby examples/client.rb` |
| **C#** | `examples/DojutsuClient.cs` | `dotnet run` |

## Provider switch (any language)

The `provider` and `model` params work identically in all languages:

```
args = ["your task", "api_key", "groq",        "moonshotai/kimi-k2-instruct-0905"]
args = ["your task", "api_key", "openai",       "gpt-4o"]
args = ["your task", "api_key", "anthropic",    "claude-opus-4-5"]
args = ["your task", "api_key", "mistral",      "mistral-large-latest"]
args = ["your task", "api_key", "openrouter",   "openai/gpt-4o"]
args = ["your task", "api_key", "huggingface",  "mistralai/Mistral-7B-Instruct-v0.3"]
```
