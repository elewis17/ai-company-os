# Workflow: Incident Response

## Purpose

Define the controlled process for responding to production incidents, service disruptions, and system failures.

This workflow ensures:

- incidents are identified quickly
- mitigation occurs rapidly
- ownership is clear
- system stability is restored safely
- root causes are identified
- long-term improvements are captured

Incident response protects the reliability and integrity of production systems.

---

# Core Principles

1. Production stability takes priority over feature development.
2. Clear ownership is required during incident response.
3. Mitigation should occur before deep investigation.
4. Root causes must be identified before closing incidents.
5. Incidents must generate learning and improvement tasks.
6. Transparency and documentation are required throughout the response process.

---

# Roles in this Workflow

**Incident Commander (usually Project Manager or Technical Architect)**

- coordinates incident response
- assigns responsibilities
- maintains situational awareness

**Software Engineer**

- investigates system behavior
- applies mitigation or fixes
- validates system stability

**QA Analyst**

- confirms issue reproduction
- validates system recovery
- verifies regression safety

**Technical Architect**

- supports root cause analysis
- validates system-level implications

**Founder**

- informed for major incidents
- approves major emergency decisions if required

---

# Workflow Steps

---

## 1. Incident Detection

Owner: Software Engineer or Monitoring System  
Next Owner: Incident Commander

Incidents may be detected through:

- monitoring alerts
- system errors
- user reports
- regression failures
- performance degradation

Initial information should include:

- affected systems
- observed symptoms
- time of occurrence

Exit Criteria

A confirmed incident is identified and escalated.

---

## 2. Incident Triage

Owner: Incident Commander  
Next Owner: Software Engineer

The Incident Commander evaluates severity:

Severity levels may include:

Critical  
- production outage
- data corruption risk
- major user impact

High  
- major feature failure
- significant performance degradation

Medium  
- partial feature impact
- limited user disruption

Low  
- minor issues or cosmetic defects

Response priority is assigned based on severity.

Exit Criteria

Incident severity is classified and response actions are defined.

---

## 3. Mitigation

Owner: Software Engineer  
Next Owner: QA Analyst

The immediate goal is to restore service.

Mitigation may include:

- rolling back a deployment
- disabling a feature flag
- restarting services
- isolating failing components
- applying temporary patches

Mitigation should prioritize speed and stability.

Exit Criteria

Service stability is restored or impact is significantly reduced.

---

## 4. Verification of System Stability

Owner: QA Analyst  
Next Owner: Technical Architect

QA confirms that:

- the system behaves normally
- core functionality is restored
- regressions are not introduced
- monitoring signals return to normal ranges

Exit Criteria

System stability is confirmed.

---

## 5. Root Cause Analysis

Owner: Technical Architect  
Next Owner: Project Manager

The Technical Architect leads investigation of:

- underlying cause
- architectural weaknesses
- contributing factors

This analysis should determine:

- why the incident occurred
- why safeguards failed
- how similar incidents can be prevented

Exit Criteria

Root cause is documented.

---

## 6. Post-Incident Improvement Planning

Owner: Project Manager  
Next Owner: Assigned Agent

The Project Manager converts lessons learned into improvement tasks.

Possible improvements include:

- architecture changes
- monitoring improvements
- testing improvements
- deployment safeguards
- documentation updates

Tasks must be created using:

`schemas/task_contract.json`

Exit Criteria

Improvement tasks are recorded and scheduled.

---

## 7. Incident Closeout

Owner: Incident Commander  
Next Owner: None

The Incident Commander confirms:

- system stability restored
- root cause documented
- improvement tasks scheduled
- incident summary recorded

Exit Criteria

Incident is formally closed.

---

# Rework Routing Rules

If root cause unclear → Technical Architect  
If mitigation fails → Software Engineer  
If verification fails → QA Analyst  
If improvement tasks unclear → Project Manager  

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
