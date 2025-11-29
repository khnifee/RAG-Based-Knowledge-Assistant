# Contributing to RAG-Based Knowledge Assistant

Thank you for your interest in contributing to the **RAG-Based Knowledge Assistant** project.
This repository follows a clean, modular architecture and aims to provide an extensible reference implementation for Retrieval-Augmented Generation (RAG) systems. Contributions that improve reliability, performance, and architecture are welcome.

Please read the guidelines below before submitting code, documentation, or feature proposals.

---

## 1. Getting Started

### Fork the Repository
Fork the repository to your GitHub account and clone your fork locally:

```bash
git clone https://github.com/<your-username>/RAG-Based-Knowledge-Assistant.git
cd RAG-Based-Knowledge-Assistant
```

### Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 2. Branching Strategy

All changes must be made on a dedicated feature branch:

```bash
git checkout -b feature/<short-description>
```

Examples:
- feature/vector-db-support
- feature/add-tests-for-ingestion
- fix/chunking-bug

Direct pushes to `main` are restricted by branch protection rules.  
All updates must go through a Pull Request.

---

## 3. Code Style & Standards

- Follow **PEP8** style guidelines.
- Use **type hints** for all Python functions.
- Keep modules small and cohesive.
- Avoid unnecessary abstraction; clarity over cleverness.
- Ensure new code includes structured logging where appropriate.

---

## 4. Testing

This project uses **pytest** for unit and integration tests.

Before submitting a Pull Request:

```bash
pytest -v
```

Add tests for:
- New services  
- Database interactions  
- API routes  
- Edge cases (e.g., empty documents, malformed input)

Pull Requests without tests may not be accepted.

---

## 5. Commit Conventions

Follow conventional commits:

- feat: new feature
- fix: bug fix
- docs: documentation changes
- test: adding or updating tests
- refactor: restructuring code without behavior change
- chore: tooling, cleanup, CI updates

Example:

```
feat(embedding): add support for sentence-transformer models
```

---

## 6. Pull Request Guidelines

Before submitting a PR:

1. Ensure your branch is up to date with main:
   ```bash
   git pull origin main
   ```

2. Confirm all tests pass locally.

3. Provide a clear PR description including:
   - What problem it solves  
   - Summary of changes  
   - Any breaking changes  
   - Links to related issues

4. Keep PRs small and focused. Avoid combining unrelated changes.

---

## 7. Documentation Contributions

Documentation improvements are welcome.  
This includes updates to:

- README.md
- Architecture diagrams
- API docs
- Examples and usage guides

Please update relevant documentation when modifying code.

---

## 8. Issue Reporting

When reporting bugs, include:

- Detailed, descriptive title  
- Steps to reproduce  
- Expected vs actual behavior  
- Environment details (OS, Python version, dependencies)  
- Logs or stack traces if available  

Feature requests should include:

- Motivation  
- Use cases  
- Suggested approach (optional)

---

## 9. Security Policy

If you discover a security issue, do **not** open a public GitHub issue.  
Instead, email:

**baba.tauseef41@gmail.com**

We will coordinate responsible disclosure.

---

## 10. License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve this project.  
Your contributions make the RAG ecosystem stronger.
