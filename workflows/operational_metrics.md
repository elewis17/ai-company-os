# Workflow: Operational Metrics

## Purpose

Define how the organization measures engineering performance, system reliability, and operational health.

This workflow ensures:

- execution performance is visible
- system health is continuously monitored
- process improvements are informed by real data
- leadership can assess organizational effectiveness

Operational metrics provide feedback loops for continuous improvement.

---

# Core Principles

1. Metrics must reflect meaningful operational outcomes.
2. Metrics should guide improvement, not create bureaucracy.
3. Only a small set of high-signal metrics should be tracked.
4. Data should be reviewed regularly to identify trends.
5. Metrics should trigger improvement actions when thresholds are crossed.

---

# Roles in this Workflow

**Project Manager**

- tracks execution metrics
- monitors delivery performance
- identifies workflow bottlenecks

**Technical Architect**

- monitors system health metrics
- evaluates reliability trends

**QA Analyst**

- tracks quality metrics
- identifies defect patterns

**Founder**

- reviews overall organizational performance

---

# Key Metrics

## Delivery Metrics

Tracked by Project Manager:

- task cycle time
- tasks completed per sprint
- blocked task frequency
- review turnaround time

---

## Quality Metrics

Tracked by QA Analyst:

- defect rate
- regression frequency
- PR rework rate
- test coverage trends

---

## Reliability Metrics

Tracked by Technical Architect:

- incident frequency
- mean time to recovery (MTTR)
- deployment failure rate
- rollback frequency

---

## System Health Metrics

Tracked by Technical Architect:

- system error rates
- latency trends
- resource utilization
- uptime

---

# Workflow Steps

---

## 1. Metric Collection

Owner: Project Manager / Technical Architect / QA Analyst  
Next Owner: Project Manager

Each responsible role collects relevant metrics during normal operations.

Metrics may be sourced from:

- CI pipelines
- monitoring systems
- issue tracking
- task systems

Exit Criteria

Metrics data is collected and updated.

---

## 2. Metric Review

Owner: Project Manager  
Next Owner: Technical Architect

Metrics are reviewed to identify:

- operational trends
- performance degradation
- delivery bottlenecks
- quality regressions

Exit Criteria

Potential issues or improvement opportunities are identified.

---

## 3. Operational Health Assessment

Owner: Technical Architect  
Next Owner: Project Manager

The Technical Architect evaluates whether trends indicate:

- architecture weaknesses
- reliability risks
- infrastructure limitations

Exit Criteria

System health assessment is documented.

---

## 4. Improvement Identification

Owner: Project Manager  
Next Owner: Assigned Agent

If issues are identified, improvement tasks are created using:

`schemas/task_contract.json`

Improvements may include:

- workflow adjustments
- architecture changes
- testing improvements
- monitoring enhancements

Exit Criteria

Improvement tasks are created and scheduled.

---

## 5. Leadership Review

Owner: Founder  
Next Owner: Project Manager

The Founder reviews key operational metrics to confirm:

- organizational performance
- engineering effectiveness
- delivery health

Exit Criteria

Leadership visibility is maintained.

---

# Rework Routing Rules

If metrics unclear → Project Manager  
If system health risk identified → Technical Architect  
If quality degradation detected → QA Analyst  

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
