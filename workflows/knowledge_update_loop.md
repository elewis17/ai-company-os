# Workflow: Knowledge Update Loop

## Purpose

Ensure the organization remains aligned with meaningful improvements in engineering practice, architecture, security, and delivery without chasing trends or introducing unnecessary complexity.

This workflow allows the system to improve over time while preserving stability, consistency, and operational simplicity.

---

# Core Principles

1. Only material improvements should trigger change.
2. New tools, practices, or patterns must solve a real problem.
3. Architectural stability is preferred over novelty.
4. Major changes require Founder approval.
5. Approved changes must be converted into planned work through the normal workflow system.
6. Documentation must be updated before the change is considered complete.

---

# Roles in this Workflow

**Technical Architect**
- monitors relevant technical changes
- evaluates architectural relevance
- prepares improvement proposals

**Project Manager**
- converts approved changes into planned work
- sequences implementation tasks
- tracks execution

**Founder**
- approves major architectural or operational changes

**Software Engineer / QA Analyst**
- surface repeated implementation or quality pain points
- provide feedback on recurring friction

---

# Workflow Steps

## 1. Monitor for Material Changes

**Owner:** Technical Architect  
**Next Owner:** Technical Architect

The Technical Architect monitors:

- evolving engineering best practices
- relevant framework updates
- security standards
- platform changes
- infrastructure improvements
- repeated internal execution pain points

Examples of valid triggers:

- repeated delivery friction
- recurring quality failures
- security exposure
- maintainability degradation
- meaningful reliability issues

**Exit Criteria**

A specific improvement opportunity is identified and described clearly enough to evaluate.

---

## 2. Evaluate Relevance

**Owner:** Technical Architect  
**Next Owner:** Technical Architect or Founder

Before recommending change, the Technical Architect evaluates:

- development speed improvement
- maintainability improvement
- reliability improvement
- security improvement
- operational simplicity
- migration cost
- disruption risk

Changes must not be proposed solely because they are popular, new, or fashionable.

**Exit Criteria**

The change is classified as either:
- no action
- minor improvement
- major change

---

## 3. Prepare Proposal

**Owner:** Technical Architect  
**Next Owner:** Founder or Technical Architect

If action is warranted, the Technical Architect prepares a short proposal containing:

- proposed change
- problem being solved
- expected benefits
- risks
- migration impact
- affected repository areas
- recommendation: approve or decline

**Exit Criteria**

Proposal is complete and ready for decision.

---

## 4. Approval Decision

**Owner:** Technical Architect or Founder  
**Next Owner:** Project Manager or Technical Architect

Approval path:

**Minor improvements**
- approved by Technical Architect

**Major architectural or operating model changes**
- escalated to Founder for approval

Possible outcomes:
- approve
- reject
- request revision
- defer

**Exit Criteria**

A clear decision exists.

---

## 5. Convert Approved Change into Planned Work

**Owner:** Project Manager  
**Next Owner:** Assigned Agent

If approved, the Project Manager converts the change into formal work using the normal planning process.

This includes:
- defining required tasks
- sequencing dependencies
- assigning owners
- using `schemas/task_contract.json` where implementation work is required

Approved changes may not be executed informally outside the standard workflow system.

**Exit Criteria**

Approved change is represented as planned, assigned work.

---

## 6. Update Documentation

**Owner:** Technical Architect  
**Next Owner:** Project Manager

The Technical Architect updates affected documentation before or alongside implementation as appropriate.

Possible updates include:

- `architecture/system_architecture.md`
- `architecture/coding_standards.md`
- `architecture/security_principles.md`
- `architecture/repo_structure.md`
- ADRs
- related workflow documentation

**Exit Criteria**

Documentation accurately reflects the approved direction.

---

## 7. Closeout Review

**Owner:** Project Manager  
**Next Owner:** None

Project Manager confirms:

- approved changes were planned correctly
- related work is scheduled or completed
- documentation is updated
- deferred items are tracked separately

**Exit Criteria**

Change is operationally integrated or formally deferred.

---

# Rework Routing Rules

If proposal is incomplete → Technical Architect  
If change is too disruptive → Founder  
If execution planning is unclear → Project Manager  
If documentation is incomplete → Technical Architect

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
