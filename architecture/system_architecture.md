# System Architecture Principles

This document defines the architectural model used across the repository.

The goal is to maintain a system that is:

- predictable
- maintainable
- easy to reason about
- safe to evolve over time

Architecture should optimize for long-term clarity rather than short-term convenience.

---

# Default Application Shape

Most applications built in this repository follow this stack:

Frontend
- TypeScript
- React
- Vite or Next.js depending on deployment needs

Backend
- Supabase
- PostgreSQL
- Edge Functions when server logic is required

Authentication
- Managed authentication provider
- Row Level Security (RLS) used to enforce access policies

Deployment
- Vercel or Cloudflare depending on the application

Telemetry / Observability
- OpenTelemetry
- structured logs
- error tracking where appropriate

This stack provides a balance of developer velocity, reliability, and scalability.

---

# Architectural Philosophy

The system follows a layered architecture designed to keep responsibilities clearly separated.

Key goals:

- isolate business logic from UI
- make data access explicit
- avoid hidden coupling
- maintain predictable data flow

Code should be organized so that developers can quickly understand:

- where logic belongs
- where data originates
- where changes should be made safely

---

# System Layers

Applications follow a layered structure.

## 1. UI Layer

Purpose:
- presentation
- user interaction
- visual state

Responsibilities:
- rendering components
- handling user input
- invoking application logic through hooks

Constraints:
- no direct database access
- no business logic
- minimal state orchestration

UI should remain thin and focused on presentation.

---

## 2. Application Layer (Hooks)

Purpose:
- orchestrate UI state
- coordinate user interactions
- connect UI to domain logic

Responsibilities:
- state management
- side effects
- calling services
- managing UI behavior

Hooks act as the bridge between the UI and domain logic.

Examples:

- data loading
- user interaction flows
- optimistic updates

---

## 3. Domain / Services Layer

Purpose:
- implement business logic
- orchestrate external services
- enforce system rules

Responsibilities:

- business rules
- domain calculations
- service orchestration
- interaction with APIs

Services should remain independent from UI concerns.

They should be testable and reusable.

Examples:

- pricing logic
- analytics calculations
- financial modeling
- deal evaluation
- workflow orchestration

---

## 4. Data Layer

Purpose:
- interact with persistent storage

Responsibilities:

- database queries
- migrations
- data validation
- access policies
- schema definitions

This layer includes:

- Supabase queries
- database migrations
- RLS policies
- schema definitions

All database access must pass through this layer.

---

# Data Flow

The system follows a predictable flow of data.

UI Component  
→ Hook / Application Layer  
→ Service / Domain Logic  
→ Data Layer / Database

Responses follow the reverse path.

Database  
→ Service  
→ Hook  
→ UI

This structure prevents hidden dependencies and keeps logic organized.

---

# Architecture Guardrails

The following rules protect the integrity of the architecture.

These should not be violated.

## UI Rules

- UI components must not call the database directly
- UI components must not implement business logic
- UI components should remain presentation focused

## Domain Logic Rules

- business logic must live in services or domain modules
- services must not depend on UI components

## Data Access Rules

- database access must be centralized
- queries should not be scattered across the codebase
- schema changes must go through migrations

## Dependency Direction

Dependencies should flow downward:

UI  
→ Application Layer  
→ Domain Layer  
→ Data Layer

Lower layers should never depend on higher layers.

---

# Architectural Decision Documentation

Any change that affects core architecture must be documented.

Examples include:

- database schema changes
- authentication model changes
- deployment model changes
- core system architecture changes

These changes require:

- PRD linkage
- architecture note
- tests
- explicit review signoff

This prevents undocumented architectural drift.

---

# Evolution of the Architecture

The system should evolve intentionally.

When architecture becomes difficult to reason about:

- refactor modules
- clarify boundaries
- simplify dependencies

Avoid accumulating hidden complexity.

The goal is a system that remains understandable even as it grows.

---

# Final Principle

Architecture exists to make the system easier to build, maintain, and evolve.

If a change makes the system harder to understand or maintain, it should be reconsidered before being introduced.
