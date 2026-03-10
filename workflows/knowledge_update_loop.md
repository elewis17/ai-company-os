# Workflow: Knowledge Update Loop

## Purpose

Ensure the organization continuously improves its engineering practices, architecture, and operational model without chasing trends or introducing unnecessary complexity.

This workflow allows the system to evolve deliberately while preserving architectural stability and execution reliability.

---

# Core Principles

1. Improvements must solve a real operational problem.
2. Architectural stability is preferred over novelty.
3. Changes must produce measurable improvement in reliability, maintainability, speed, or security.
4. Major architectural changes require Founder approval.
5. Approved improvements must be converted into planned work.
6. Documentation must be updated before the change is considered complete.

---

# Roles in this Workflow

**Technical Architect**

- monitors emerging practices and platform changes  
- evaluates potential improvements  
- prepares improvement proposals  

**Project Manager**

- converts approved improvements into planned work  
- sequences implementation tasks  
- tracks execution  

**Founder**

- approves major architectural or operating model changes  

**Software Engineer / QA Analyst**

- surface recurring engineering or quality friction during development

---

# Workflow Steps

---

## 1. Monitor for Improvement Opportunities

**Owner:** Technical Architect  
**Next Owner:** Technical Architect  

The Technical Architect continuously monitors for relevant changes in:

- engineering best practices
- framework updates
- security standards
- infrastructure improvements
- platform capabilities
- repeated development friction
- recurring quality failures

Examples of valid triggers:

- slow development cycles
- repeated defects
- excessive complexity
- maintenance burden
- reliability risks
- security concerns

**Exit Criteria**

A specific improvement opportunity is clearly identified.

---

## 2. Evaluate Relevance

**Owner:** Technical Architect  
**Next Owner:** Technical Architect or Founder  

The Technical Architect evaluates whether the improvement meaningfully impacts:

- development speed
- maintainability
- reliability
- security
- operational simplicity
- long-term scalability

The evaluation must consider:

- migration cost
- disruption risk
- compatibility with existing architecture

**Exit Criteria**

The change is classified as one of:

- no action required  
- minor improvement  
- major change  

---

## 3. Prepare Improvement Proposal

**Owner:** Technical Architect  
**Next Owner:** Founder or Technical Architect  

The Technical Architect prepares a proposal containing:

- proposed change
- problem being solved
- expected benefits
- risks
- migration impact
- affected repository areas
- recommended action

**Exit Criteria**

Proposal is complete and ready for approval.

---

## 4. Approval Decision

**Owner:** Technical Architect or Founder  
**Next Owner:** Project Manager or Technical Architect  

Approval path:

**Minor improvements**  
Approved by Technical Architect.

**Major architectural or operational changes**  
Escalated to Founder for approval.

Possible outcomes:

- approve  
- reject  
- request revision  
- defer  

**Exit Criteria**

A clear decision has been recorded.

---

## 5. Convert Approved Change Into Planned Work

**Owner:** Project Manager  
**Next Owner:** Assigned Agent  

If approved, the Project Manager converts the change into formal work through the normal planning process.

This includes:

- defining implementation tasks
- sequencing dependencies
- assigning owners
- creating task contracts using `schemas/task_contract.json`

Approved improvements may not be implemented outside the standard workflow system.

**Exit Criteria**

Approved changes are represented as scheduled tasks.

---

## 6. Documentation Update

**Owner:** Technical Architect  
**Next Owner:** Project Manager  

Before or during implementation, the Technical Architect updates affected documentation.

Possible updates include:

- `architecture/system_architecture.md`
- `architecture/coding_standards.md`
- `architecture/security_principles.md`
- `architecture/repo_structure.md`
- architecture decision records
- related workflow documentation

**Exit Criteria**

Documentation accurately reflects the approved direction.

---

## 7. Closeout Review

**Owner:** Project Manager  
**Next Owner:** None  

The Project Manager confirms:

- approved improvements were converted into planned work
- documentation has been updated
- implementation tasks are scheduled or completed
- deferred improvements are tracked separately

**Exit Criteria**

Improvement is integrated into the organization’s operating model or formally deferred.

---

# Rework Routing Rules

If proposal incomplete → Technical Architect  
If proposal too disruptive → Founder  
If implementation planning unclear → Project Manager  
If documentation incomplete → Technical Architect  

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
