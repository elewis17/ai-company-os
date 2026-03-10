# Coding Standards

This document defines the coding philosophy and conventions used across the codebase.  
The goal is to maintain clarity, maintainability, and predictable structure while avoiding unnecessary complexity or fragmentation.

---

# Core Philosophy

Code should be:

- Easy to read
- Easy to scan quickly
- Easy to modify safely
- Easy to reason about

Prefer clarity over cleverness.  
Prefer simple structure over abstract architecture.

When making design decisions, optimize for the developer who must maintain the code 6–12 months later.

---

# General Principles

- Prefer readable, explicit code over clever or condensed code
- Use strong typing wherever possible
- Keep functions focused and composable
- Remove dead or unused code quickly
- Minimize hidden side effects
- Avoid premature abstraction
- Favor predictable patterns across the codebase

---

# Cohesion vs Fragmentation

Related logic should remain grouped together when doing so improves readability.

Avoid splitting files purely to keep them small.

Over-fragmentation creates:

- unnecessary navigation
- cognitive overhead
- harder code discovery

Instead:

- keep cohesive logic together
- split files when separation improves clarity or ownership

Good reasons to split a file:

- a module has multiple distinct responsibilities
- a section becomes difficult to scan
- logic needs independent testing
- a piece of code becomes reusable across features

---

# File Length Guidance

File length is a warning signal, not a strict rule.

Typical guidance:

| Size | Interpretation |
|-----|---------------|
| under ~200 lines | usually fine |
| 200–400 lines | review structure |
| 400–500 lines | ensure strong cohesion |
| 500+ lines | likely needs decomposition |

Large files are acceptable if they remain easy to scan and clearly structured.

Avoid mechanical splitting that harms readability.

---

# Top-Level Orchestration

A file should expose a clear top-level flow.

A reader should be able to quickly understand:

- what the file does
- the main execution path
- the important behaviors

Supporting implementation details should be:

- placed below the main flow, or
- extracted into helpers/services when they obscure understanding.

Think of the top of the file as the orchestrator view.

---

# Responsibility Separation

Keep responsibilities clearly separated.

Typical separation pattern:

| Responsibility | Location |
|----------------|---------|
| UI / presentation | components |
| reusable UI behavior | hooks |
| data access / API calls | services |
| business rules | domain modules |
| shared utilities | utils |
| type definitions | types |

Avoid mixing UI code with heavy business logic or data access.

---

# TypeScript / TSX Guidelines

## Components

- Components should remain presentation-focused
- Avoid embedding heavy business logic inside UI components
- Prefer one component per file
- Small composition helpers may live in the same file

## Hooks

Hooks encapsulate reusable UI state or behavior.

Examples include:

- data fetching
- event handling logic
- shared component behavior

Hooks should follow the naming pattern:

useSomething

---

# Naming Conventions

| Element | Convention |
|-------|-----------|
| Components | PascalCase |
| Hooks | useSomething |
| Services | descriptive domain names |
| Utility functions | action-oriented names |
| Database objects | explicit and stable naming |

Examples:

UserCard.tsx  
usePropertyData.ts  
dealAnalyzerService.ts  
calculateCashFlow.ts

Avoid vague names like:

helpers.ts  
utils2.ts  
misc.ts

---

# Comments

Comments should explain why, not what.

Avoid narrating obvious code.

Good uses of comments:

- explaining architectural decisions
- describing non-obvious constraints
- clarifying complex business rules

Example:

```ts
// We round here because downstream reporting expects whole-dollar values
```

Avoid:
// increment i by one
i++

# Dead Code Policy

Dead code should be removed quickly.

Avoid leaving:
 - unused functions
 - commented-out code blocks
 - outdated logic paths

Git history preserves previous versions when needed.

# Testing Expectations

Testing should focus on logic that could break.

Guidelines:

- New feature logic should include tests when practical
- Regression bugs should include a regression test
- Critical flows should have end-to-end coverage

Testing priorities:
- Business logic
- calculation correctness
- core user flows
- Maintainability Rule

When modifying existing code:
- leave the code clearer than you found it
- reduce complexity where possible
- improve naming when it increases clarity

Small continuous improvements prevent architectural decay.

# Final Guideline

If code becomes:
- hard to scan
- hard to explain
- hard to test
- hard to review safely

it should be refactored before it grows further.

