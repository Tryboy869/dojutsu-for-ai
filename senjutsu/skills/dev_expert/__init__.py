"""Built-in dev-expert skill content."""

SKILL_CONTENT = '''---
name: dev-expert
description: "Apply BEFORE any coding task. Forces AI to think like an expert full-stack developer: domain identification, stack selection, security, SEO, architecture, subdomains standards, scalability."
---

# DEV EXPERT — Expert Full Stack Developer Mindset

## Core Principle
An expert dev does NOT code immediately.
They UNDERSTAND first, ARCHITECT second, CODE last.

---

## PHASE 1 — DOMAIN IDENTIFICATION

Identify the exact domain before anything:
- **SaaS**: Multi-tenant, robust auth, billing
- **E-commerce**: Cart, payments, inventory, taxes
- **Portfolio/Landing**: SEO critical, performance, static preferred
- **API/Backend**: Contracts, versioning, rate limiting
- **AI Application**: Latency, token cost, fallbacks
- **Dashboard/Analytics**: Real-time, aggregations, charts
- **Internal tools**: Simple UX, maintainability

### Subdomains and their standards:
- **Auth**: JWT + refresh tokens / OAuth2 — never store passwords in plain text
- **Payments**: Stripe/Paddle — never handle cards yourself — PCI-DSS
- **Files**: S3 equivalent — never local in production — signed URLs
- **Search**: Elasticsearch/Typesense/Algolia — avoid LIKE %query% SQL
- **Email**: Resend/SendGrid — SPF/DKIM/DMARC — bounce handling
- **Real-time**: WebSockets/SSE — reconnection, offline state, backpressure

---

## PHASE 2 — STACK SELECTION (in order of priority)

1. **Team & maintenance** — Can this stack be maintained long-term?
2. **Domain fit** — Some stacks are better for certain domains
3. **Performance requirements** — Real-time? Static? CPU-intensive?
4. **Expected scale** — 100 users or 1M users?
5. **Time to market** — Speed vs perfection

### Stack by use case:
- **Static portfolio/landing**: HTML/CSS vanilla, or Astro, NEVER React SPA
- **SaaS Frontend**: Next.js (App Router) + TailwindCSS + shadcn/ui + Zod
- **API Backend**: Python → FastAPI; Node → Hono or Fastify (NOT Express in 2025)
- **Database**: PostgreSQL by default; SQLite for serverless edge; Redis for cache/sessions
- **ORM**: Drizzle (modern, typed) or Prisma for Node; SQLAlchemy 2.0 for Python
- **Auth**: NextAuth v5 / Clerk / Supabase Auth — NEVER implement own session mgmt
- **Deploy**: Vercel/CF Pages for frontend; Railway/Render/Fly.io for backend

---

## PHASE 3 — ARCHITECTURE

### Patterns by scale:
- **Solo/startup (< 10k users)**: Modular monolith — NO premature microservices
- **Growth (10k-1M users)**: Domain-driven splitting, strategic cache, CDN
- **Scale (> 1M users)**: Justified microservices, event-driven, CQRS if needed

### Non-negotiable architecture rules:
- **Separation of concerns**: UI ≠ business logic ≠ data access
- **Config by environment**: NEVER hardcoded URLs/keys
- **Error boundaries**: Each layer handles its errors cleanly
- **Idempotence**: Critical operations must be replayable

---

## PHASE 4 — SECURITY (by design)

10 absolute rules:
1. **Input validation everywhere** — Validate AND sanitize all inputs (Zod, Pydantic)
2. **HTTPS mandatory** — Even in local dev for cookies
3. **Secrets in env vars** — NEVER in code, NEVER in git
4. **Least privilege** — Each service accesses only what it needs
5. **SQL Injection impossible** — ORM or parameterized queries only
6. **XSS prevention** — CSP headers, HTML sanitization
7. **CSRF protection** — CSRF tokens, SameSite cookies
8. **Rate limiting** — On ALL public routes and auth routes
9. **Audit trail** — Log sensitive actions (who did what and when)
10. **Dependency updates** — Dependabot active, no abandoned deps

Essential security headers:
- Content-Security-Policy
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security (HSTS)

---

## PHASE 5 — SEO (when applicable)

HTML checklist:
- `<title>` unique per page (50-60 chars)
- `<meta description>` unique (150-160 chars)
- Single `<h1>` per page, hierarchy H1 > H2 > H3
- `alt` on all images, descriptive URLs

Core Web Vitals:
- LCP < 2.5s: optimize images, preload critical fonts
- INP < 100ms: no blocking JS
- CLS < 0.1: reserve space for images/ads

OpenGraph + Structured data (JSON-LD) required.

---

## PHASE 6 — PERFORMANCE

- Index ALL columns used for search/join
- Pagination on all lists (NEVER SELECT * without LIMIT)
- N+1 queries = bug, not a feature (eager loading, DataLoader)
- Connection pooling configured
- Code splitting by route
- Bundle size < 200kb gzipped for first load

---

## ANTI-PATTERNS FORBIDDEN

- ❌ "Works locally" without Docker/reproducible env
- ❌ console.log/print in production
- ❌ TODO in production for > 30 days
- ❌ Copy-paste code > 10 lines without abstraction
- ❌ Disable CORS completely (*) in production
- ❌ Hardcode secrets in code
- ❌ "We'll handle security later"
- ❌ Deploy without tests
- ❌ Version node_modules / __pycache__ / .env
- ❌ Framework X "because it's trending" without business justification

---

## PRE-CODE CHECKLIST

Before writing the first line:
- [ ] Domain identified
- [ ] Subdomains listed with standards
- [ ] Stack chosen with justification
- [ ] Architecture decided
- [ ] Security planned from start
- [ ] SEO relevant? Checklist activated
- [ ] Performance requirements clear
- [ ] File structure defined
- [ ] Secrets in env vars
- [ ] Tests planned from the start
'''
