# Repo Structure

## Purpose

This document defines the default repository structure for applications and operating-system files in this repository.

The goals of the structure are:

- clarity
- scanability
- consistency
- maintainability
- intuitive discovery for both humans and agents

A good repository structure should make it easy to answer:

- where new code should go
- where existing logic lives
- where documentation belongs
- where architectural rules are defined
- where agents should look before making changes

The repository should feel organized, predictable, and easy to navigate without requiring tribal knowledge.

---

# Core Principles

1. Organize by responsibility first, not by personal preference.
2. Prefer predictable folder names across projects.
3. Keep related logic grouped together when that improves discovery.
4. Avoid scattering business logic across UI folders.
5. Avoid creating excessive micro-files and micro-folders with no real structural value.
6. Documentation and operational rules should live in stable, top-level locations.
7. A developer or agent should be able to scan the repository quickly and infer where work belongs.

---

# Top-Level Repository Structure

A typical repository should be organized like this:

```text
src/
public/
supabase/

architecture/
company/
agents/
workflows/
templates/
schemas/
reports/
docs/

tests/               (optional, if not colocated)
scripts/             (optional)
```
This structure is intended to balance:

discoverability

separation of concerns

pragmatic cohesion

# src/ Folder Responsibilities

## components/

Contains reusable UI components and presentation primitives.

Examples:

- buttons
- cards
- tables
- shared layout pieces
- reusable composed UI sections

Rules:

- components should remain presentation-focused
- shared primitives should not accumulate hidden business logic
- generic UI building blocks belong here, not inside arbitrary feature folders

---

## features/

Contains bounded feature-level folders.

A feature folder may include:

- feature-specific UI
- feature-specific hooks
- feature-specific types
- tests
- local helpers

Use features/ when a feature has enough surface area to justify keeping related pieces together.

Example structure:

src/features/deal-analysis/
  components/
  hooks/
  types/
  utils/
  tests/

Rules:

- feature folders should remain bounded and understandable
- do not duplicate shared primitives already defined elsewhere
- feature folders may compose pieces from components/, hooks/, services/, domain/, and types/

---

## hooks/

Contains reusable application or UI behavior.

Examples:

- data loading hooks
- reusable stateful UI logic
- interaction flow hooks

Rules:

- hooks should not become a dumping ground for all logic
- reusable hooks belong here
- feature-specific hooks may live inside the feature folder when they are tightly scoped

---

## services/

Contains service-layer logic and external orchestration.

Examples:

- API integration
- Supabase interaction wrappers
- external service clients
- backend orchestration helpers

Rules:

- services should not contain presentation logic
- services may coordinate external systems
- services should remain testable and explicit

---

## domain/

Contains business rules and domain logic.

Examples:

- calculations
- scoring logic
- transformations
- core product rules
- financial modeling rules

Rules:

- domain logic must remain independent from UI concerns
- domain modules should be reusable and testable
- if the logic expresses business meaning, it likely belongs here instead of lib/

---

## lib/

Contains shared low-level helpers and internal utilities.

Examples:

- formatting helpers
- parsing utilities
- generic utility wrappers
- shared technical helpers

Rules:

- lib/ should remain generic
- do not place business logic here
- do not allow lib/ to become a vague miscellaneous dumping ground

If something has domain meaning, move it to domain/ or services/.

---

## pages/

Contains route-level page components or screens.

Rules:

- pages should compose behavior rather than contain heavy business logic
- pages should coordinate components, hooks, and feature modules
- pages should remain easy to scan

For routing-based applications, this is where top-level user-facing screens live.

---

## styles/

Contains shared styling assets.

Examples:

- global CSS
- design tokens
- shared style configuration
- theme-level styling assets

---

## types/

Contains shared type definitions.

Examples:

- domain models
- shared interfaces
- API contract types
- common payload shapes

Rules:

- keep shared types here when they are used broadly
- feature-local types may remain inside a feature folder when tightly scoped

---

# Structure Rules

## Rule 1: Keep shared things truly shared

Shared primitives belong in stable shared folders.

Examples:

- shared UI primitives → components/
- shared business rules → domain/
- shared low-level helpers → lib/

Do not place broadly reused code inside random feature folders.

---

## Rule 2: Keep business logic out of pages and components

Business logic belongs in:

- domain/
- services/
- application hooks when appropriate

Pages and components should primarily compose behavior, not define core rules.

---

## Rule 3: Feature folders are allowed, but they must stay bounded

Feature folders are useful when they improve discoverability.

They should not become mini-monoliths with unclear internal structure.

Use them when they help answer:

- what belongs to this feature
- what is shared vs local
- where a future change should go

---

## Rule 4: Prefer predictable naming across repositories

Use stable names like:

- components
- features
- hooks
- services
- domain
- types

Avoid creative or inconsistent folder naming that forces people or agents to relearn the structure each time.

---

## Rule 5: Colocate when it improves clarity, centralize when it improves reuse

Not all code should be globally centralized.

Use colocation when logic is tightly bound to a feature.

Use shared top-level folders when logic is reused broadly.

The decision should improve scanability, not ideology.

---

## Rule 6: Avoid miscellaneous dump folders

Avoid vague names like:

- misc
- helpers
- stuff
- shared2
- common_temp

Every folder should have a clear purpose that can be explained in one sentence.

---

## Rule 7: Optimize for scanning

A future developer or agent should be able to:

- find the app entry path quickly
- locate business logic without searching the whole repo
- identify architectural rules at the top level
- distinguish feature-local code from shared code
- understand where to place new code without guessing

If the structure makes that hard, the structure needs improvement.

---

# Human and Agent Accessibility

This repository is designed to be read and operated by both humans and agents.

That means the structure should support:

- fast scanning
- obvious folder intent
- stable naming
- low ambiguity
- easy routing of work to the correct file or folder

Agents should not need hidden knowledge to infer:

- where UI work goes
- where business logic goes
- where workflow docs live
- where architecture rules live
- where schemas and templates live

The repository itself should communicate these boundaries clearly.

---

# Evolution Rules

The structure may evolve, but changes should be deliberate.

A structural change is justified when it materially improves:

- scanability
- maintainability
- architectural clarity
- reuse
- onboarding
- agent execution reliability

Do not reorganize folders casually.

Repository structure changes should be made carefully because they affect:

- code discovery
- workflow references
- agent execution patterns
- documentation accuracy

Major structure changes should be reflected in:

- architecture/repo_structure.md
- related workflow documentation
- any impacted templates or agent instructions

---

# Standard of Judgment

A good repo structure should make the right place for a new change feel obvious.

If developers or agents regularly ask:

- where should this file go?
- should this live in a page, hook, service, or util?
- where are the system rules documented?
- where do I find workflow instructions?

then the structure is not yet good enough.

The best repository structure is not the most clever.

It is the one that makes work easy to find, easy to place, and easy to maintain.
