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
- completed

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

##Handoff

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

---

## Agent Handoff Payload Checklist

Purpose: Ensure every workflow handoff transfers clear ownership using canonical fields and roles.

Include the following fields and values exactly in each handoff payload:

- next_owner: one of [product_manager, project_manager, technical_architect, software_engineer, qa_analyst]
- next_required_action: a concise imperative describing what the next owner must do next
- status: one of [ready for next stage, blocked, requires revision, completed]
- workflow_outcome: one of [continue, blocked, completed]
- execution_mode: one of [planning, review, implementation]
- summary: 1–3 sentences summarizing the step outcome
- artifacts_updated:
  - If no repository changes in this step: ["No repository artifacts updated in this stage"]
  - If repository changes were applied: list the exact file paths updated
- decision_or_outcome: bullets of key decisions or outcomes (optional but recommended)
- blockers_or_risks: bullets of known blockers or risks (optional)
- completed_work: short list of what was done in this step (optional)
- implementation_plan: when planning implementation; include goal, issue_body, recommended_first_changes, notes
- file_operations: only when execution_mode = implementation; list the exact operations to apply (write_file, append_file, replace_in_file)
- debug: optional fields such as instructions_loaded (boolean) and retrieved_file_count (integer)

Rules reminders:
- Use only canonical role IDs listed above; do not invent new roles.
- Do not change field names.
- If file_operations are provided, execution_mode must be implementation and artifacts_updated must list exact paths.
- If no repository changes are proposed, execution_mode must be planning or review and artifacts_updated must be ["No repository artifacts updated in this stage"].
- Self-handoffs are only allowed when status is completed or blocked.
## Usage

- When transferring ownership to another role, copy the Handoff Checklist and include it in the handoff note or issue/PR comment.
- Fill all required fields and use only canonical role IDs.
- Template: [Handoff Checklist](./handoff_checklist.md)

### Usage Example

Example handoff fields:

```
next_owner: software_engineer
next_required_action: "Implement minimal doc updates for process_change handoffs per standard"
status: ready for next stage
```

### Quick Checklist

- Include next_owner and next_required_action in every handoff
- Allowed next_owner values: product_manager, project_manager, technical_architect, software_engineer, qa_analyst
- Do not self-handoff unless status is completed or blocked
- Keep changes minimal; reference the standard, do not restate it elsewhere

---

## Process Change Handoff Example

A minimal, schema-compliant handoff payload for a process_change step:

```json
{
  "agent": "software_engineer",
  "status": "ready for next stage",
  "workflow_outcome": "continue",
  "execution_mode": "planning",
  "summary": "Prepared a minimal documentation update proposal for process_change.",
  "artifacts_updated": ["No repository artifacts updated in this stage"],
  "next_required_action": "Validate alignment with architecture/standards and approve or request revision.",
  "handoff": {
    "next_owner": "technical_architect",
    "next_required_action": "Validate alignment with architecture/standards and approve or request revision."
  }
}
```

## Valid next_owner roles

Use only these canonical role IDs:

- product_manager
- project_manager
- technical_architect
- software_engineer
- qa_analyst

## Guidance for process_change

Prefer the smallest targeted documentation or process changes necessary to address the specific issue; avoid broad refactors, do not introduce new features or change product strategy under this workflow, and escalate only according to the established escalation rules. For routing, prefer transferring ownership among technical_architect, project_manager, software_engineer, and qa_analyst; involve product_manager only when product-scope clarification is required.
