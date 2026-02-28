/**
 * Dojutsu-for-AI — TypeScript client (Node.js)
 * Requires: no extra deps — uses built-in `net` module
 *
 * Prerequisites:
 *   git clone https://github.com/Tryboy869/dojutsu-for-ai
 *   cd dojutsu-for-ai && python allpath-runner.py daemon &
 */
import * as net from "net";

interface DojutsuResult {
  byakugan: string;
  mode_sage: string;
  jougan: string;
  execution: string;
  skills_used: string[];
  total_time: number;
}

function dojutsu(fn: string, args: string[] = []): Promise<DojutsuResult> {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection("/tmp/allpath_runner.sock");
    const chunks: Buffer[] = [];

    socket.setTimeout(120_000);
    socket.on("connect", () => {
      socket.write(
        JSON.stringify({ package: "dojutsu-agent", function: fn, args })
      );
    });
    socket.on("data",  (chunk) => chunks.push(chunk));
    socket.on("end",   () => resolve(JSON.parse(Buffer.concat(chunks).toString())));
    socket.on("error", reject);
    socket.on("timeout", () => { socket.destroy(); reject(new Error("Timeout")); });
  });
}

// ── Usage ─────────────────────────────────────────────────────────────
const GROQ_KEY = process.env.GROQ_API_KEY ?? "";

// Full pipeline — Groq + Kimi
const result = await dojutsu("run", [
  "Build a rate limiter middleware for Express using Redis sliding window",
  GROQ_KEY,
  "groq",
  "moonshotai/kimi-k2-instruct-0905",
]);
console.log("=== BYAKUGAN ===\n", result.byakugan);
console.log("=== CODE ===\n", result.execution);
console.log("Skills used:", result.skills_used);

// Quick structural analysis only (1 LLM call)
const analysis = await dojutsu("byakugan", [
  "Add WebSocket support to an existing FastAPI app",
  GROQ_KEY,
  "groq",
]);
console.log("Structural vision:", analysis.byakugan);

// Skill count
const info = await dojutsu("skills_count", []);
console.log(`${info.count} skills indexed`);
