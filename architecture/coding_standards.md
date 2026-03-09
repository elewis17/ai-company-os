# Coding Standards

## General
- Prefer readable, explicit code over clever code
- Use strong typing
- Keep functions focused and composable
- Remove dead code quickly
- Minimize side effects

## TS / TSX rules
- TSX files should stay presentation-focused
- Business logic belongs in hooks, services, or domain modules
- Prefer one component per file unless composition is trivial
- Prefer type-only imports where applicable
- Avoid giant files; refactor when a file becomes hard to scan

## Naming
- Components: PascalCase
- hooks: useSomething
- services: domain-oriented and descriptive
- utility functions: action-oriented and specific
- database objects: explicit and stable naming

## Comments
- Comment why, not what
- Avoid narrating obvious code
- Add short file headers only when they materially help maintenance

## Test expectations
- New feature logic requires tests
- Regression bugs require a regression test when practical
- End-to-end tests cover core user flows
