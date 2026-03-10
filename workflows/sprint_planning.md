# Workflow: Sprint Planning

## Purpose

Define how work is selected, sequenced, and committed for the next execution cycle.

This workflow ensures:

- the highest-value work is prioritized
- agents are not overloaded
- dependencies are respected
- execution progress remains predictable
- delivery capacity is used effectively

Sprint Planning translates approved product scope into scheduled work.

---

# Core Principles

1. Only approved PRDs enter sprint planning.
2. Work must be represented as task contracts.
3. Dependencies must be respected when sequencing work.
4. Specialists must not be overloaded.
5. High-value, low-ambiguity work is prioritized.
6. Capacity must include buffer for defects and review cycles.

---

# Roles in this Workflow

**Founder**

- defines strategic priorities

**Product Manager**

- ensures backlog aligns with product direction

**Project Manager**

- leads sprint planning
- schedules work
- assigns owners
- manages execution capacity

**Technical Architect**

- validates architectural feasibility of planned work

---

# Workflow Steps

---

## 1. Backlog Review

Owner: Product Manager  
Next Owner: Project Manager

The Product Manager reviews the backlog and ensures it contains:

- approved PRDs
- clearly defined scope
- prioritized product work

Incomplete or ambiguous backlog items must be refined before planning.

Exit Criteria

Backlog contains only approved and well-defined work.

---

## 2. Capacity Assessment

Owner: Project Manager  
Next Owner: Technical Architect

The Project Manager evaluates available execution capacity including:

- agent availability
- known blockers
- review cycles
- QA capacity
- expected overhead

A buffer should be reserved for:

- defects
- CI failures
- review iterations

Exit Criteria

Realistic execution capacity is established.

---

## 3. Technical Feasibility Check

Owner: Technical Architect  
Next Owner: Project Manager

The Technical Architect reviews planned work to confirm:

- architecture compatibility
- dependency readiness
- technical feasibility

If major architecture changes are required, the work may be:

- deferred
- broken into smaller tasks
- routed through the knowledge update loop

Exit Criteria

Planned work is technically feasible.

---

## 4. Task Definition

Owner: Project Manager  
Next Owner: Assigned Agent

The Project Manager converts backlog items into executable tasks using:

`schemas/task_contract.json`

Each task must define:

- objective
- scope
- out-of-scope boundaries
- dependencies
- acceptance criteria
- owner role

Exit Criteria

All planned work exists as task contracts.

---

## 5. Task Assignment

Owner: Project Manager  
Next Owner: Assigned Agent

Tasks are assigned based on:

- agent specialization
- dependency order
- workload balance

No agent should be assigned more work than capacity allows.

Exit Criteria

Every planned task has an assigned owner.

---

## 6. Sprint Commitment

Owner: Project Manager  
Next Owner: Founder

The Project Manager defines the sprint commitment including:

- sprint goal
- committed tasks
- owners
- identified risks

Founder reviews the sprint plan for alignment with strategic priorities.

Exit Criteria

Sprint scope is confirmed.

---

## 7. Sprint Kickoff

Owner: Project Manager  
Next Owner: Assigned Agents

The Project Manager communicates the sprint plan and confirms:

- task assignments
- sequencing
- dependencies
- expected outcomes

Execution begins following the Feature Development workflow.

Exit Criteria

Sprint execution begins.

---

# Rework Routing Rules

If backlog item unclear → Product Manager  
If capacity unrealistic → Project Manager  
If architecture conflict → Technical Architect  
If task definition unclear → Project Manager  

---

# Handoff Requirement

Each stage of this workflow must follow the standard defined in:

`workflows/handoff_standard.md`

A stage is not considered complete until a valid handoff exists containing:

- status
- completed work
- artifacts updated
- next owner
- next required action
- blockers or risks
