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

tests/        (optional)
scripts/      (optional)

Not every project will require every folder, but the naming and intent should remain consistent.

---

# Top-Level Folder Responsibilities

## src/

Contains application source code.

This is where product logic, UI, domain logic, and internal utilities live.

---

## public/

Contains static assets served directly by the frontend application.

Examples:

- images
- icons
- public metadata
- favicon files
- robots.txt

No application logic should be placed here.

---

## supabase/

Contains Supabase backend infrastructure.

Examples:

- migrations
- SQL schema
- RLS policies
- edge functions
- Supabase configuration

This folder represents the data infrastructure layer of the system.

---

## architecture/

Contains architectural standards and technical rules.

Examples:

- system_architecture.md
- repo_structure.md
- coding_standards.md
- security_principles.md

These files define how systems should be built and maintained.

---

## company/

Contains company-level strategy and organizational direction.

Examples:

- company vision
- product strategy
- internal principles

This folder explains why the organization builds what it builds.

---

## agents/

Contains agent role definitions and operational boundaries.

Examples:

- agent responsibilities
- capability definitions
- execution constraints
- agent instructions

Agents should be able to read this folder to understand their responsibilities within the operating system.

---

## workflows/

Contains execution workflows and operational processes.

Examples:

- sprint planning
- feature development
- pull request review
- release management
- incident response
- operational metrics

This folder defines how work moves through the organization.

---

## templates/

Contains reusable templates for structured documents.

Examples:

- PRD templates
- task briefs
- architecture decision records
- report templates

Templates support consistent execution across the system.

---

## schemas/

Contains machine-readable schemas used for structured inputs or outputs.

Examples:

- task schemas
- workflow payload schemas
- reporting schemas

Schemas help standardize structured communication for both humans and agents.

---

## reports/

Contains generated or periodic reports.

Examples:

- weekly reports
- executive summaries
- operational metrics reports
- incident reports

Reports represent outputs rather than governing rules.

---

## docs/

Contains supporting documentation not tied directly to architecture or workflows.

Examples:

- onboarding documentation
- product reference material
- implementation notes

This folder should not become a dumping ground for unrelated files.

---

## tests/

Optional folder for cross-feature or integration tests when they are not colocated.

Examples:

- integration tests
- end-to-end tests
- system-level tests

---

## scripts/

Optional folder for repository automation scripts.

Examples:

- setup scripts
- development utilities
- migration helpers
- reporting tools

Scripts should support operations but not replace architecture or domain logic.

---

# Source Code Structure

Inside `src/`, code should follow a predictable internal structure.

Recommended layout:

src/
  assets/
  components/
  features/
  hooks/
  services/
  domain/
  integrations/
  context/
  lib/
  pages/
  styles/
  types/

This structure balances:

- discoverability
- separation of concerns
- pragmatic cohesion

---

# src/ Folder Responsibilities

## assets/

Contains static assets used by the application.

Examples:

- images
- icons
- fonts
- visual resources used by the UI

Assets should not contain application logic.

---

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

Use features/ when a feature has enough surface area to justify grouping related pieces together.

Example:

src/features/deal-analysis/
  components/
  hooks/
  types/
  utils/
  tests/

Rules:

- feature folders should remain bounded and understandable
- avoid duplicating shared primitives already defined elsewhere
- feature folders may compose pieces from components/, hooks/, services/, domain/, and types/

---

## hooks/

Contains reusable application or UI behavior.

Examples:

- data loading hooks
- reusable state logic
- interaction flow hooks

Rules:

- hooks should not become a dumping ground
- reusable hooks belong here
- feature-specific hooks may remain inside feature folders when tightly scoped

---

## services/

Contains service-layer logic and external orchestration.

Examples:

- API integration
- Supabase service wrappers
- backend interaction utilities
- external service clients

Rules:

- services should not contain presentation logic
- services should remain explicit and testable

---

## domain/

Contains business rules and domain logic.

Examples:

- financial calculations
- scoring models
- transformation logic
- product rules

Rules:

- domain logic must remain independent of UI concerns
- domain modules should be reusable and testable

---

## integrations/

Contains integration adapters for external systems.

Examples:

- Supabase integration
- third-party APIs
- analytics providers
- external data services

Integrations isolate external dependencies from the rest of the system.

---

## context/

Contains React context providers and global state containers.

Examples:

- authentication context
- application state context
- shared runtime state

Context should be used carefully to avoid hidden coupling.

---

## lib/

Contains shared low-level utilities.

Examples:

- formatting helpers
- parsing utilities
- generic helpers

Rules:

- lib/ should remain generic
- business logic should not live here

If logic expresses domain meaning, move it to domain/.

---

## pages/

Contains route-level pages or application screens.

Rules:

- pages should orchestrate components and hooks
- pages should not contain heavy business logic
- pages should remain easy to scan

---

## styles/

Contains shared styling assets.

Examples:

- global CSS
- design tokens
- theme configuration

---

## types/

Contains shared type definitions.

Examples:

- domain models
- API payload shapes
- shared interfaces

Feature-specific types may remain within feature folders when appropriate.

---

# Structure Rules

## Rule 1: Keep shared things truly shared

Shared primitives belong in stable shared folders.

Examples:

- shared UI primitives → components/
- shared business rules → domain/
- shared helpers → lib/

Avoid placing broadly reused code inside random feature folders.

---

## Rule 2: Keep business logic out of pages and components

Business logic belongs in:

- domain/
- services/
- hooks when appropriate

Pages and components should compose behavior, not define core rules.

---

## Rule 3: Feature folders must stay bounded

Feature folders improve discoverability but must remain understandable.

They should help answer:

- what belongs to this feature
- what logic is shared
- where future changes belong

---

## Rule 4: Prefer predictable naming

Use stable names like:

components  
features  
hooks  
services  
domain  
types

Avoid creative folder names that increase cognitive load.

---

## Rule 5: Colocate when helpful, centralize when reusable

Not all logic should be centralized.

Use colocation for feature-specific code.

Use shared folders for broadly reused logic.

---

## Rule 6: Avoid miscellaneous folders

Avoid vague names such as:

misc  
helpers  
stuff  
shared2  

Every folder should have a clear, explainable purpose.

---

## Rule 7: Optimize for scanning

A developer or agent should be able to quickly:

- locate the UI entry point
- find business logic
- find architecture rules
- identify feature boundaries
- determine where new code should go

If that is difficult, the structure should be improved.

---

# Human and Agent Accessibility

This repository is designed for both human and agent interaction.

The structure should support:

- fast scanning
- clear folder intent
- predictable naming
- minimal ambiguity

Agents should not require hidden knowledge to determine:

- where UI logic lives
- where business logic lives
- where workflows live
- where architecture rules live

The repository structure itself should communicate these boundaries.

---

# Evolution Rules

Repository structure may evolve, but changes must be deliberate.

Structural changes should only occur when they materially improve:

- maintainability
- clarity
- scanning
- reuse
- onboarding
- agent reliability

Major changes should update:

- architecture/repo_structure.md
- related workflow documentation
- affected templates or agent instructions

---

# Standard of Judgment

A strong repository structure makes the correct location for new work obvious.

If developers or agents frequently ask:

- where should this file go?
- where is the business logic?
- where are the architecture rules?

then the structure needs improvement.

The best repository structure is not the most clever.

It is the one that makes work easy to find, easy to place, and easy to maintain.
