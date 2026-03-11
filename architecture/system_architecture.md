# System Architecture

## Purpose

This document defines the default target architecture for applications built in this repository.

It exists to create a system that is:

- predictable
- maintainable
- easy to reason about
- safe to evolve over time

This document describes the architectural standard new work should follow.

Existing applications in the repository may not yet fully conform to this structure.  
Where that is true, the expectation is to move them toward this architecture over time through normal feature work and targeted refactoring.

---

# Architectural Philosophy

The default architecture should optimize for:

- clear separation of responsibilities
- predictable data flow
- minimal hidden coupling
- maintainability over time
- ease of scanning and understanding the codebase

The system should make it obvious:

- where UI logic belongs
- where business logic belongs
- where data access belongs
- where architectural changes must be made carefully

The goal is not abstraction for its own sake.  
The goal is a codebase that remains understandable as it grows.

---

# Default Application Shape

Applications in this repository will typically follow this shape:

Frontend
- TypeScript
- React
- Vite by default unless another frontend framework is intentionally chosen

Backend / Data
- Supabase
- PostgreSQL
- Edge Functions where server-side logic is required

Authentication
- managed authentication
- RLS / RBAC where applicable

Deployment
- deployment approach may vary by project
- current projects may use GitHub Pages or other deployment targets depending on needs

Observability
- logging, error tracking, and telemetry should be added where appropriate
- observability tooling is project-specific unless explicitly standardized

---

# Target Layered Architecture

Applications should follow a layered structure.

## 1. UI Layer

Purpose:
- presentation
- rendering
- user interaction

Responsibilities:
- display data
- collect user input
- invoke application behavior through hooks or handlers

Constraints:
- no direct database calls
- no embedded business logic
- no hidden service orchestration

The UI layer should stay focused on presentation and interaction.

---

## 2. Application Layer

Purpose:
- orchestrate state and user-driven behavior

Typical implementation forms:
- hooks
- controllers
- feature-level state modules

Responsibilities:
- coordinate UI state
- handle side effects
- manage interaction flow
- call domain or service logic

This layer acts as the bridge between the UI and the business/domain layer.

---

## 3. Domain / Services Layer

Purpose:
- implement business logic
- enforce application rules
- orchestrate external service behavior

Responsibilities:
- business calculations
- decision rules
- domain transformations
- integration orchestration

Examples:
- financial calculations
- lease analysis rules
- deal evaluation
- scenario modeling
- cross-service workflows

This layer must remain independent from UI concerns.

---

## 4. Data Layer

Purpose:
- interact with persistence and external data systems

Responsibilities:
- database queries
- schema definitions
- migrations
- access policies
- repository/data-access functions
- external API persistence logic where applicable

Constraints:
- data access should be explicit
- schema changes must go through controlled migrations
- access rules must be enforced at the proper boundary

All persistent data interaction should flow through this layer.

---

# Default Data Flow

The intended data flow is:

UI  
→ Application Layer  
→ Domain / Services Layer  
→ Data Layer

Responses flow back upward:

Data Layer  
→ Domain / Services Layer  
→ Application Layer  
→ UI

This structure exists to avoid:

- business logic leakage into components
- direct database access from UI
- hidden dependencies between unrelated modules
- hard-to-trace side effects

---

# Architectural Guardrails

The following rules are mandatory for the target architecture.

## UI Rules

- UI components must not call the database directly
- UI components must not contain core business logic
- pages and components should remain presentation-focused

## Application Layer Rules

- application-layer code should coordinate behavior, not store core business rules
- state orchestration should remain separate from rendering

## Domain Rules

- business logic belongs in domain modules or services
- domain logic should be reusable and testable
- domain logic must not depend on UI components

## Data Rules

- data access should be centralized and explicit
- queries should not be scattered across the UI
- schema and policy changes must be reviewed carefully

## Dependency Direction Rules

Dependencies should flow downward only:

UI  
→ Application Layer  
→ Domain / Services Layer  
→ Data Layer

Lower layers must not depend on higher layers.

---

# Current-State Reality vs Target-State Standard

This repository may contain applications or modules that were built quickly and do not yet fully conform to this architecture.

That does not invalidate the standard.

Instead:

- new work should follow this architecture
- refactors should move existing code toward this structure
- major monolithic areas should be reduced over time when doing so materially improves maintainability

The architecture standard defines the direction of travel, not a false claim that all existing code is already cleanly structured.

---

# Change Policy

Any change that materially affects:

- data model
- security model
- authentication boundaries
- deployment architecture
- major module boundaries
- core system behavior

requires:

- PRD linkage where applicable
- architecture documentation update
- tests
- explicit review signoff

Major architectural changes must not happen silently.

---

# Architectural Evolution

The architecture should evolve deliberately.

Refactor toward better structure when:

- business logic is leaking into UI
- data access is scattered
- files or modules become difficult to scan
- dependencies become confusing
- responsibilities are mixed together

Do not introduce complexity just to appear architectural.

Prefer the simplest structure that preserves:

- clarity
- separation of concerns
- safe changeability
- long-term maintainability

---

# Standard of Judgment

When choosing between two architectural approaches, prefer the one that is:

- easier to understand
- easier to test
- easier to change safely
- more consistent with repository patterns
- less likely to create hidden coupling

The best architecture is not the most abstract.  
It is the one that keeps the system understandable as it grows.
