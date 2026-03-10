# Standard: Documentation Ownership

## Purpose

Ensure documentation remains organized, current, and owned by the appropriate role.

Clear ownership prevents documentation decay and ensures agents always operate using reliable, current information.

---

# Core Principles

1. Every documentation domain must have a clear owner.
2. Documentation must be updated when the underlying system changes.
3. Each topic should have one authoritative source.
4. Documentation must be easy to understand and easy to navigate.
5. Ownership does not permit unapproved scope expansion.
6. Domain owners are responsible for correctness within their area.

---

# Ownership by Role

## Founder

Responsible for approving major changes to high-level company direction and operating model documentation when required.

Primary areas:
- major company direction changes
- major operating model changes

---

## Product Manager

Responsible for product-facing planning and definition documents.

Primary areas:
- `company/company_vision.md`
- `company/product_strategy.md`
- PRDs created from `templates/prd_template.md`
- roadmap and milestone definitions where applicable

---

## Technical Architect

Responsible for technical standards and architecture documentation.

Primary areas:
- `architecture/system_architecture.md`
- `architecture/repo_structure.md`
- `architecture/coding_standards.md`
- `architecture/security_principles.md`
- architecture decision records

---

## Project Manager

Responsible for workflow and execution-process documentation.

Primary areas:
- `workflows/`
- delivery process documents
- coordination and operational execution procedures

---

## QA Analyst

Responsible for quality-related process documentation where such documents exist.

Primary areas:
- QA procedures
- test review guidance
- quality validation standards

If no separate QA standards directory exists, these documents should remain within the approved repository structure.

---

## Software Engineer

Responsible for implementation-adjacent documentation accuracy.

Primary responsibilities:
- updating documentation when implementation changes behavior
- keeping inline documentation accurate
- ensuring usage examples remain correct
- surfacing documentation gaps to the appropriate owner

Software Engineers do not define architecture standards, but they must update implementation-linked documentation when changes are made.

---

# Documentation Update Rules

Documentation must be updated when any of the following change:

- architecture
- system behavior
- APIs or interfaces
- workflows
- testing expectations
- repository structure
- operating procedures

Failure to update documentation creates long-term operational risk.

---

# Ownership Conflict Rules

If a documentation change spans multiple domains:

- the domain owner of the primary affected area is responsible for coordination
- the Technical Architect resolves architecture-document conflicts
- the Project Manager resolves workflow-document conflicts
- the Product Manager resolves product-definition conflicts
- major cross-domain conflicts escalate to the Founder when necessary

---

# Quality Standards

Documentation should be:

- clear
- concise
- accurate
- easy to navigate
- written in simple language

Avoid:

- unnecessary verbosity
- outdated information
- duplicate sources for the same topic
- ambiguous ownership

Prefer one authoritative source per topic.

---

# Workflow Integration Rule

Documentation updates triggered by feature work, pull requests, architecture changes, or release changes must be enforced through the relevant workflow.

Documentation is not optional follow-up work when the underlying system has changed.
