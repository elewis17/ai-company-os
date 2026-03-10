# Workflow: Pull Request Review

## Purpose

Define the standard process for reviewing pull requests before code is merged into the repository.

This workflow ensures:

- code changes match approved scope
- architecture standards are maintained
- security risks are caught
- test coverage remains strong
- documentation stays accurate

Pull request review protects the integrity of the repository and prevents scope creep, architectural drift, and low-quality changes.

---

# Core Principles

1. All code changes must be traceable to an approved task contract.
2. Pull requests must stay within the scope of the assigned task.
3. Architectural boundaries must be enforced during review.
4. Tests must accompany functional changes.
5. Security-sensitive changes require careful review.
6. Documentation must be updated when behavior changes.
7. The Project Manager maintains visibility over PR progress.

---

# Roles in this Workflow

**Software Engineer**
- submits pull request

**QA Analyst**
- validates behavior and tests

**Technical Architect**
- ensures architectural integrity

**Project Manager**
- ensures PR aligns with task scope and workflow

**Founder**
- final approval authority when required

---

# Pull Request Workflow

---

## 1. Pull Request Creation

**Owner:** Software Engineer  
**Next Owner:** Project Manager

The Software Engineer submits a pull request.

The PR must include:

- description of changes
- linked task contract
- linked PRD if applicable
- summary of behavior changes
- testing notes

The PR must clearly reference the originating task defined by:

`schemas/task_contract.json`

**Exit Criteria**

PR contains clear traceability to the assigned task.

---

## 2. Task Traceability Validation

**Owner:** Project Manager  
**Next Owner:** Technical Architect

The Project Manager confirms:

- the PR maps to an approved task
- the scope matches the task contract
- the PR does not introduce unrelated work
- dependencies between tasks are respected

If scope expansion is detected, the PR is returned to the Software Engineer.

**Exit Criteria**

PR scope aligns with the approved task contract.

---

## 3. Architecture Review

**Owner:** Technical Architect  
**Next Owner:** QA Analyst

The Technical Architect reviews the PR for alignment with repository architecture.

Validation includes:

- directory placement aligns with `architecture/repo_structure.md`
- coding standards follow `architecture/coding_standards.md`
- system design aligns with `architecture/system_architecture.md`
- security practices follow `architecture/security_principles.md`
- business logic remains in appropriate layers
- UI layers do not contain core business logic

If architectural violations are found, the PR is returned for revision.

**Exit Criteria**

Architecture integrity confirmed.

---

## 4. QA Validation

**Owner:** QA Analyst  
**Next Owner:** Software Engineer or CI

QA reviews:

- feature behavior
- acceptance criteria
- regression risks
- edge cases

QA also evaluates:

- adequacy of test coverage
- correctness of tests
- reproducibility of results

Possible outcomes:

- pass
- rework required
- blocked

Rework returns to the Software Engineer.

**Exit Criteria**

QA approval.

---

## 5. Continuous Integration Validation

**Owner:** Software Engineer  
**Next Owner:** Founder or Project Manager

CI checks must pass:

- lint
- build
- test suite
- type checks

If CI fails, work returns to the Software Engineer.

**Exit Criteria**

All automated checks pass.

---

## 6. Documentation Verification

**Owner:** Project Manager  
**Next Owner:** Founder

The Project Manager confirms documentation is updated when necessary.

Potential updates include:

- architecture documentation
- workflow documentation
- templates
- operational documentation
- release notes

Documentation updates must occur when the PR changes behavior, interfaces, or processes.

**Exit Criteria**

Documentation accurately reflects the implemented behavior.

---

## 7. Final Approval

**Owner:** Founder  
**Next Owner:** Project Manager

The Founder reviews the PR for:

- scope alignment
- architectural safety
- overall quality
- readiness for merge

Possible outcomes:

- approve
- request changes
- reject due to architectural or quality violations

**Exit Criteria**

Merge approved.

---

## 8. Merge and Closeout

**Owner:** Project Manager

Project Manager confirms:

- PR merged successfully
- related tasks marked complete
- follow-up work captured as new tasks if needed

The feature workflow continues or concludes based on remaining tasks.

---

# Mandatory Review Checks

Every PR must confirm the following:

- task traceability exists
- scope matches assigned task
- naming and structure are consistent
- business logic is not leaking into UI layers
- tests are adequate
- CI checks pass
- security-sensitive changes are reviewed
- documentation updated when necessary

---

# Rework Routing Rules

If scope mismatch → Project Manager  
If architecture violation → Technical Architect  
If QA failure → Software Engineer  
If CI failure → Software Engineer  
If documentation missing → Project Manager  
If final approval fails → return to relevant upstream owner

---

#. Founder Preview Review

**Owner:** Project Manager  
**Next Owner:** Founder

Before final approval, the Project Manager provides the Founder with:

- pull request link
- preview link or clear local preview instructions
- short summary of the feature
- expected behaviors to verify
- confirmation that architecture review, QA review, and CI checks have passed

The Founder reviews the feature as a product experience, not as a code reviewer.

The Founder validates:

- feature behavior matches the PRD
- user-visible behavior is acceptable
- the feature is ready to ship

**Exit Criteria**

Founder has enough visibility to make a product approval decision.

## 7. Final Approval

**Owner:** Founder  
**Next Owner:** Project Manager

The Founder reviews the feature preview and confirms:

- delivered behavior matches approved scope
- the feature is acceptable for release
- no visible issues block shipment

Possible outcomes:

- approve
- request changes
- reject due to product readiness concerns

**Exit Criteria**

Merge approved.
---

# Summary

Pull request review flows through:

Software Engineer → Project Manager → Technical Architect → QA Analyst → CI → Founder → Project Manager

Each stage protects the repository from drift, scope creep, and quality regressions.
