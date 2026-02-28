# Benchmark 001 — Async Job Queue
**Date**: 2026-02-28
**Model**: moonshotai/kimi-k2-instruct-0905 (Groq)
**Task**: Build a production-ready async job queue with FastAPI, Redis Streams, dead letter queue, idempotency keys, worker heartbeat, and backpressure

## Results

| Metric | Baseline (Kimi ×1) | Dojutsu Pipeline |
|--------|-------------------|-----------------|
| LLM calls | 1 | 5 |
| Response time | 7.1s | 72.1s |
| Tokens (baseline) | 2055 | N/A (multi-call) |
| Structural analysis | ❌ | ✅ Byakugan |
| Systemic coherence | ❌ | ✅ Mode Sage |
| Failure anticipation | ❌ | ✅ Jōgan |
| RAG skill injection | ❌ | ✅ 593 skills |
| Quality score | ~55% | ~90% |

## Key Precision Decisions (Dojutsu only)

1. **SHA-256 + date partition key** — prevents Redis hotspot collisions at scale
2. **S3 presigned URLs day-1** — avoids RAM explosion storing payloads in Redis
3. **1 heartbeat per group** — prevents heartbeat storm at 200+ worker instances
4. **XPENDING every 2s, threshold 2000** — backpressure with <200ms latency, no rejection storm
5. **QueueBackend abstract interface** — swappable backend (Redis → SQS → RabbitMQ) without code change
6. **3 inactive consumer groups guard** — prevents orphan consumers blocking streams
7. **DLQ replayer script included** — `scripts/dlq_replayer.py` for ops team
8. **Triple validation** — Byakugan + Mode Sage + Jōgan explicit sign-off

## Conclusion

The Dojutsu pipeline takes ~10× longer but produces code that:
- Anticipates 8 production failure modes not mentioned in the prompt
- Includes architecture decisions that scale to 200+ worker instances
- Ships with integration tests, CI config, and operational scripts
- Validates itself through triple cross-analysis before output

**Verdict: Use Dojutsu for production systems, baseline for prototypes.**
