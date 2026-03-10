# Workflow Handoff Standard

## Purpose

Ensure clear ownership transfer between agents during workflow execution.

Autonomous organizations fail when work is completed but responsibility for the next step is unclear.

This standard ensures every workflow stage ends with a clear operational handoff.

---

# Required Handoff Fields

Every workflow stage must produce a handoff containing the following information.

### Status
One of:

- ready for next stage
- blocked
- requires revision

### Completed Work

What was accomplished during the stage.

### Artifacts Updated

List of files or repository areas that were modified.

Examples:

- PRD
- architecture docs
- source code
- tests
- workflows
- templates

### Decision or Outcome

Key decisions made during the stage.

### Next Owner

Which role is responsible for the next step.

Example roles:

- Product Manager
- Project Manager
- Technical Architect
- Software Engineer
- QA Analyst
- Founder

### Next Required Action

What the next owner must do.

### Blockers or Risks

Any issues that may prevent progress.

---

# Handoff Template

Handoff

Completed By:
<Role>

Status:
ready for next stage | blocked | requires revision

Completed Work
- ...

Artifacts Updated
- ...

Decision or Outcome
- ...

Next Owner
- ...

Next Required Action
- ...

Blockers or Risks
- ...

---

# Workflow Rule

A workflow stage may not begin until the previous stage has produced a valid handoff.

The handoff must clearly identify:

- the current status
- work completed
- artifacts updated
- the next owner
- the next required action
- blockers or risks

Workflows that reference this standard must enforce this rule.
