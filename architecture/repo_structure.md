# Repo Structure

Suggested layout:

src/
  components/
  features/
  hooks/
  services/
  domain/
  lib/
  pages/
  styles/
  types/

docs/
company/
architecture/
agents/
workflows/
reports/

## Structure rules
- Shared primitives go in components/lib, not random feature folders
- Domain logic belongs in domain or services, not pages
- Feature folders may compose UI, hooks, tests, and types for bounded features
- Prefer predictable folder names across products for reuse
