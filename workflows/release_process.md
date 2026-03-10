# Workflow: Release Process

## Purpose

Define the controlled process for deploying validated software changes to production.

This workflow ensures:

- only approved features are released
- deployments are stable and reversible
- regressions are detected quickly
- users receive reliable software updates

Release management protects the reliability and integrity of the production system.

---

# Core Principles

1. Only approved and tested work may be released.
2. Continuous integration must pass before release.
3. Every release must have a rollback path.
4. Release notes must document behavior changes.
5. Production systems must be monitored after deployment.
6. Failures must trigger immediate investigation.

---

# Roles in this Workflow

**Software Engineer**

- prepares release artifacts
- ensures build readiness

**QA Analyst**

- confirms feature validation
- verifies regression safety

**Project Manager**

- coordinates release readiness
- confirms documentation and release notes

**Founder**

- provides final release approval when required

---

# Workflow Steps

---

## 1. Release Readiness Check

Owner: Project Manager  
Next Owner: QA Analyst

The Project Manager confirms that candidate features:

- passed PR review
- passed CI validation
- passed QA validation
- match approved PRDs

Exit Criteria

Release candidate features are validated.

---

## 2. QA Final Verification

Owner: QA Analyst  
Next Owner: Software Engineer

QA performs final checks including:

- behavior verification
- regression validation
- environment readiness

Exit Criteria

Release candidate confirmed safe.

---

## 3. Build Verification

Owner: Software Engineer  
Next Owner: Project Manager

The Software Engineer confirms:

- build artifacts generated successfully
- dependency versions are correct
- migrations are validated
- deployment scripts are ready

Exit Criteria

Release build verified.

---

## 4. Release Documentation

Owner: Project Manager  
Next Owner: Founder

Release notes are prepared including:

- new features
- behavior changes
- known limitations
- migration requirements if applicable

Exit Criteria

Release documentation complete.

---

## 5. Final Approval

Owner: Founder  
Next Owner: Software Engineer

Founder confirms the release is ready for deployment.

Possible outcomes:

- approve
- request delay
- request additional validation

Exit Criteria

Release approved.

---

## 6. Deployment

Owner: Software Engineer  
Next Owner: Project Manager

The Software Engineer deploys the release to production using the approved deployment process.

Exit Criteria

Deployment completed successfully.

---

## 7. Post-Release Monitoring

Owner: Project Manager  
Next Owner: Software Engineer or QA Analyst

The system is monitored for:

- errors
- performance regressions
- unexpected behavior

If issues occur, the rollback plan may be activated.

Exit Criteria

Release stability confirmed.

---

# Rework Routing Rules

If CI fails → Software Engineer  
If QA fails → Software Engineer  
If release documentation incomplete → Project Manager  
If deployment fails → Software Engineer  
If production regression detected → QA Analyst and Software Engineer  

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
