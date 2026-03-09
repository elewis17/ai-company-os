# System Architecture Principles

## Default application shape
- Frontend: TypeScript / React
- Backend: Supabase / Postgres / Edge Functions
- Auth: managed auth with RBAC/RLS where applicable
- Deployments: Vercel or Cloudflare
- Telemetry: OpenTelemetry

## Layering rules
- UI layer: presentation and interaction only
- Hooks/application layer: state orchestration and UI behavior
- Domain/services layer: business logic and external service orchestration
- Data layer: DB access, queries, policies, migrations

## Architecture guardrails
- No DB calls in UI components
- No business logic hidden inside pages/components
- No silent coupling between modules
- Every major architectural decision gets documented

## Change policy
Any change that affects data model, security, deployment, or core architecture requires:
- PRD linkage
- architecture note
- tests
- explicit review signoff
