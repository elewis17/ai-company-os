# Security Principles

## Purpose

This document defines the security principles that govern how systems in this repository must be built, deployed, and maintained.

Security should not be treated as an afterthought or a later phase of development.  
Security must be integrated into system architecture, development workflows, and operational practices.

The goal is not perfect theoretical security.  
The goal is **practical, enforceable security that prevents common failures.**

These principles apply to:

- frontend applications
- backend services
- APIs
- database systems
- infrastructure
- automation
- agent behavior

---

# Core Security Philosophy

Security failures rarely come from sophisticated attackers.

They come from predictable mistakes such as:

- exposed secrets
- overly permissive access
- unvalidated input
- insecure defaults
- forgotten endpoints
- dependency vulnerabilities

The purpose of these principles is to eliminate those predictable mistakes.

---

# Principle 1 — Least Privilege

Every system component should have **only the permissions it absolutely needs**.

Examples:

- APIs should only access the tables they require
- services should not receive full database privileges
- users should not receive admin permissions by default
- agents should only have access to the files or systems required for their role

When in doubt, grant **less access**.

Permissions can always be expanded later.

They are far harder to safely remove after systems depend on them.

---

# Principle 2 — Secure By Default

Systems must start in a secure configuration.

Developers should not need to remember to "turn security on."

Examples:

- row-level security enabled by default
- authentication required for protected endpoints
- environment variables used for secrets
- restrictive CORS policies
- minimal public exposure

If a configuration could be unsafe when misused, the default configuration should prevent that misuse.

---

# Principle 3 — No Secrets in Source Control

Secrets must **never be stored in source code repositories**.

Examples of secrets:

- API keys
- database credentials
- JWT secrets
- OAuth client secrets
- service tokens
- private certificates

Secrets must be stored using secure mechanisms such as:

- environment variables
- secret managers
- infrastructure configuration systems

If a secret is accidentally committed:

1. rotate the secret immediately
2. remove it from the repository
3. audit for potential misuse

---

# Principle 4 — Authentication Before Authorization

Systems must verify **who a user is** before deciding **what they are allowed to do**.

Authentication methods may include:

- OAuth providers
- Supabase authentication
- secure session tokens
- JWT-based authentication

Authentication must never rely on:

- client-provided identifiers
- URL parameters
- unverified cookies

Identity must always be validated by the backend.

---

# Principle 5 — Strong Authorization Controls

Authorization determines what an authenticated user is allowed to access.

Authorization should be enforced at **multiple layers**:

- API layer
- database layer
- application logic layer

For data systems, **row-level security policies** should enforce access control wherever possible.

Never assume that frontend code can enforce authorization.

Frontend code can be bypassed.

---

# Principle 6 — Validate Inputs at Trust Boundaries

All inputs entering the system must be treated as untrusted.

Inputs should be validated at system boundaries including:

- API endpoints
- form submissions
- query parameters
- uploaded files
- third-party data sources

Validation should ensure:

- expected data types
- valid ranges
- allowed formats
- safe characters

Unvalidated input is a common source of:

- injection attacks
- data corruption
- unexpected system behavior

---

# Principle 7 — Treat Public Interfaces as Hostile

Public interfaces must assume hostile interaction.

Examples of public interfaces:

- API endpoints
- authentication endpoints
- file uploads
- public query interfaces
- webhook handlers

These interfaces must assume that:

- inputs may be malicious
- requests may be automated
- attackers may probe for weaknesses

Defensive practices should include:

- input validation
- rate limiting
- authentication checks
- safe error handling

---

# Principle 8 — Log Security-Relevant Events

Systems should log events that could indicate misuse or security issues.

Examples include:

- authentication attempts
- permission failures
- suspicious API activity
- administrative actions
- system errors affecting security boundaries

Logs should support:

- debugging
- monitoring
- incident investigation

Logs should not store sensitive information such as passwords or private tokens.

---

# Principle 9 — Patch Critical Dependencies Quickly

Modern applications depend on external libraries and frameworks.

Security vulnerabilities may be discovered in those dependencies.

Repositories should:

- regularly check dependency vulnerabilities
- update critical dependencies quickly
- monitor security advisories for key frameworks

Outdated dependencies are one of the most common security risks in modern software.

---

# Principle 10 — Defense in Depth

Security should not rely on a single control.

Multiple layers of protection should exist.

Examples:

- authentication checks in APIs
- authorization rules in databases
- validation in service layers
- monitoring in infrastructure

If one control fails, others should still protect the system.

---

# Data Security Principles

Sensitive data must be handled carefully.

Examples of sensitive data include:

- personal information
- financial records
- authentication tokens
- internal operational metrics

Best practices include:

- encrypting sensitive data in transit
- restricting access using row-level security
- avoiding unnecessary data exposure
- limiting data returned by APIs

Data should only be accessible to users and systems that require it.

---

# Security Responsibilities

Security is not the responsibility of a single person.

It is the responsibility of:

- developers
- reviewers
- operators
- automation systems
- agents

Everyone interacting with the system must treat security as part of their role.

---

# Security and Agents

Agents interacting with the repository must follow the same security rules as developers.

Agents must never:

- expose secrets
- bypass authentication
- weaken security controls
- introduce insecure defaults

Agents should prioritize:

- minimal permissions
- safe configuration
- explicit authorization checks

---

# Incident Response

If a security issue is discovered:

1. contain the issue
2. prevent further exposure
3. rotate compromised credentials
4. patch the vulnerability
5. document the incident

Security incidents should be treated seriously and resolved quickly.

---

# Security Mindset

Security is not about paranoia.

It is about disciplined engineering.

The most secure systems are usually not the most complex ones.

They are the ones that:

- follow predictable rules
- enforce clear boundaries
- remove unnecessary access
- treat external input carefully

Security should be a normal part of building reliable systems.
