# Security Policy

This document outlines the security reporting policy for the **RAG-Based Knowledge Assistant** project.

We take the security of this project seriously and appreciate all responsible disclosures that help improve the safety and reliability of the system.

---

## Supported Versions

The project is under active development.  
Security updates will be applied to the latest version of the `main` branch.

| Version | Supported |
|--------|-----------|
| main    | Yes       |
| older commits | No |

---

## Reporting a Vulnerability

If you discover a security vulnerability, **do not** open a public GitHub issue.

Instead, please report it privately and responsibly by emailing:

**towseef.altaf.dev@gmail.com**

Your report should include:

- A detailed description of the vulnerability  
- Steps to reproduce (if applicable)  
- Potential impact  
- Possible mitigation ideas (optional)

You will receive acknowledgment within **48 hours** and we will work together to validate and address the issue.

---

## Disclosure Process

1. You report the issue privately.
2. We investigate and verify the vulnerability.
3. A fix is prepared on a private branch.
4. Once resolved, a patch is released publicly.
5. You may be credited in release notes if desired.

---

## Scope

This policy applies to:

- API endpoints
- Ingestion pipeline
- Vector search and embedding logic
- Database schema and migration logic
- Dependency vulnerabilities
- Authentication or authorization issues (if added later)
- Any code under this repository

This policy does **not** cover:

- Issues in external dependencies  
- Misconfigurations in user deployments  
- Third-party services (OpenAI, Qdrant, e
