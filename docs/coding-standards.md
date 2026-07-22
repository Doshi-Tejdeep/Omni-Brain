# Coding Standards

## Purpose

This document defines the coding standards for the Omni Brain project to ensure code consistency, readability, and maintainability across all team members.

---

## General Coding Rules

- Write clean, readable, and maintainable code.
- Use meaningful variable, function, and class names.
- Follow consistent indentation (4 spaces for Python).
- Remove unused code before committing.
- Add comments only where necessary to explain complex logic.

---

## Naming Conventions

### Variables
- Use descriptive names.
- Example:
  - `user_input`
  - `document_name`

### Functions
- Use lowercase with underscores.
- Example:
  - `extract_text_from_pdf()`
  - `upload_document()`

### Classes
- Use PascalCase.
- Example:
  - `DocumentProcessor`
  - `UploadManager`

### Files
- Use lowercase with hyphens or underscores.
- Examples:
  - `coding-standards.md`
  - `integration-checklist.md`

---

## Git Commit Message Format

Use clear and meaningful commit messages.

Examples:

- `feat: add PDF upload endpoint`
- `fix: resolve upload validation issue`
- `docs: add coding standards`
- `docs: update README`
- `refactor: improve document processing`

---

## Pull Request Guidelines

Before creating a Pull Request:

- Test your changes locally.
- Ensure the project builds successfully.
- Update documentation if required.
- Keep the PR focused on one feature or fix.
- Resolve merge conflicts before requesting review.

---

## Team Responsibilities

| Team Member | Responsibility |
|-------------|----------------|
| D. Tejdeep | Team Lead, Documentation, PR Review |
| Saumaditya | Backend Development |
| Pavan | Frontend Development |
| Rishi | Document Processing |
| Mariam | AI/RAG Integration |
| Teja | Database |
| Sunishka | DevOps & QA |

---

## Best Practices

- Write modular and reusable code.
- Avoid hardcoding values.
- Handle errors gracefully.
- Keep functions small and focused.
- Review code before committing.
- Follow the project folder structure.

---

## Documentation

- Update documentation whenever a new feature is added.
- Keep README files current.
- Document public APIs and important modules.

---

Maintained by: D. Tejdeep (Team Lead)
