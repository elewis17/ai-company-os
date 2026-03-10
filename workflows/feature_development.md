# Workflow: Feature Development

## Purpose

Define the standard process for converting approved product scope into implemented, validated, and documented features.

This workflow ensures:

- clear ownership at every step
- strong coordination between agents
- architecture compliance
- protection against scope creep
- clear visibility into execution progress

The **Project Manager acts as the orchestration layer** for this workflow and maintains visibility into the current state of feature delivery.

---

# Core Principles

1. No implementation begins without an approved PRD.
2. No work begins without a task contract.
3. Agents operate only within their assigned role and task scope.
4. Implementation must align with repository architecture and coding standards.
5. Scope expansion requires explicit approval.
6. The Project Manager tracks progress and identifies bottlenecks.
7. The Founder can request a feature status update from the Project Manager at any time.
8. Handoff Requirement is crucial and required to keep every future workflow informed

---

# Roles in this Workflow

**Founder**
- sets direction
- approves scope
- approves final merge

**Product Manager**
- defines product behavior
- writes PRDs
- defines acceptance criteria

**Project Manager**
- decomposes work
- assigns tasks
- tracks progress
- coordinates agents
- reports bottlenecks

**Technical Architect**
- validates architecture alignment

**Software Engineer**
- implements features

**QA Analyst**
- validates behavior and regression safety

---

# Workflow Steps

---

## 1. Direction Alignment

**Owner:** Founder  
**Next Owner:** Product Manager

Founder aligns with Product Manager on:

- feature direction
- intended outcome
- business value
- priority

**Output**

Decision to create or update a PRD.

---

## 2. Product Definition

**Owner:** Product Manager  
**Next Owner:** Founder

Product Manager creates a PRD using:

`templates/prd_template.md`

The PRD must define:

- problem statement
- desired outcome
- scope included
- scope excluded
- acceptance criteria
- constraints and assumptions
- dependencies

**Exit Criteria**

PRD is complete and ready for approval.

---

## 3. Scope Approval

**Owner:** Founder  
**Next Owner:** Project Manager

Founder reviews the PRD and either:

- approves it
- narrows scope
- requests revision
- rejects it

No downstream work proceeds without approval.

**Exit Criteria**

Approved PRD.

---

## 4. Delivery Planning

**Owner:** Project Manager  
**Next Owner:** Technical Architect

Project Manager decomposes the PRD into implementation tasks.

Each task must follow:

`schemas/task_contract.json`

Task contracts must define:

- objective
- scope
- out-of-scope boundaries
- dependencies
- owner role
- acceptance criteria

The Project Manager also determines:

- task sequencing
- dependency relationships
- potential blockers

**Exit Criteria**

A complete task set covering the PRD scope exists.

---

## 5. Architecture Review

**Owner:** Technical Architect  
**Next Owner:** Project Manager

Technical Architect reviews the PRD and task set.

Validation includes alignment with:

- `architecture/system_architecture.md`
- `architecture/repo_structure.md`
- `architecture/coding_standards.md`
- `architecture/security_principles.md`

The architect may:

- refine implementation guidance
- define interfaces
- require an architecture decision record

The architect **cannot expand product scope**.

**Exit Criteria**

Architecture is approved for implementation.

---

## 6. Task Assignment

**Owner:** Project Manager  
**Next Owner:** Assigned Agent

Project Manager assigns each task to the appropriate role.

Assignments include:

- task contract
- dependencies
- relevant files or directories
- PRD context

Agents may not expand scope or take additional work unless assigned.

**Exit Criteria**

Every task has a clear owner.

---

## 7. Implementation

**Owner:** Software Engineer  
**Next Owner:** QA Analyst

Software Engineer implements the assigned task.

Requirements:

- follow `architecture/coding_standards.md`
- stay within task contract scope
- update tests
- surface blockers to the Project Manager

If conflicts arise with requirements or architecture, work pauses and the Project Manager coordinates resolution.

**Exit Criteria**

Implementation complete and ready for QA.

---

## 8. QA Validation

**Owner:** QA Analyst  
**Next Owner:** Software Engineer or Project Manager

QA validates:

- PRD acceptance criteria
- task contract acceptance criteria
- regression safety
- behavior correctness

Possible outcomes:

- pass
- rework required
- blocked

Rework returns to the Software Engineer.

**Exit Criteria**

QA approval.

---

## 9. CI Validation

**Owner:** Software Engineer  
**Next Owner:** Founder

Continuous Integration must pass:

- lint
- tests
- build
- type checks

Failures return work to the Software Engineer.

**Exit Criteria**

All CI checks pass.

---

## 10. Merge Approval

**Owner:** Founder  
**Next Owner:** Project Manager

Founder reviews:

- PRD alignment
- implementation results
- QA outcome
- CI results
- documentation updates

Founder confirms the feature does not exceed approved scope.

**Exit Criteria**

Merge approved.

---

## 11. Documentation Updates

**Owner:** Project Manager  
**Next Owner:** None

Required documentation is updated if necessary.

Possible locations:

- `architecture/`
- `company/`
- `reports/`
- `workflows/`
- `templates/`

Release notes are created if applicable.

---

## 12. Merge and Closeout

**Owner:** Project Manager

Project Manager confirms:

- all tasks complete
- no open blockers remain
- scope delivered matches PRD
- follow-up work recorded separately

The feature is merged according to repository standards.

---

# Rework Routing Rules

If scope unclear → Product Manager  
If task unclear → Project Manager  
If architecture conflict → Technical Architect  
If QA fails → Software Engineer  
If CI fails → Software Engineer  
If merge rejected → return to appropriate upstream owner

---

# Founder Visibility

At any time the Founder can ask the Project Manager:

- what stage the feature is in
- which agent owns the next step
- which task is blocked
- where progress is stalled

The Project Manager must provide a concise execution snapshot.

Example:

Feature Status

Current Stage: Implementation  
Next Owner: Software Engineer  

Blocked Task:
Billing API integration

Bottleneck Agent:
Software Engineer


# Handoff Requirement

Each stage of this workflow must follow the standard defined in:

workflows/handoff_standard.md

No stage is considered complete until the next owner and required action are explicitly defined
