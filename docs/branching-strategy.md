# Branching Strategy

## Purpose

This document defines the Git branching strategy used in the Omni Brain project to ensure smooth collaboration and maintain code quality.

---

## Branches

### main
- Contains the stable, production-ready code.
- Only reviewed and approved changes are merged into this branch.

### develop
- Used to integrate completed features before merging into `main`.
- Developers merge approved feature branches into `develop`.

### Feature Branches

Each team member works on a separate feature branch.

| Team Member | Responsibility | Branch Name |
|-------------|----------------|-------------|
| D. Tejdeep (Team Lead) | Documentation & Project Integration | feature/team-lead |
| Saumaditya | Backend Upload API | feature/backend-upload |
| Pavan | Frontend Upload Integration | feature/frontend-upload |
| Rishi | Document Processing | feature/document-processing |
| Mariam | AI/RAG Integration | feature/ai-rag |
| Teja | Database | feature/database |
| Sunishka | DevOps & QA | feature/devops |

---

## Development Workflow

1. Create a feature branch from `develop`.
2. Implement the assigned task.
3. Test the changes locally.
4. Commit changes with a meaningful commit message.
5. Push the feature branch to GitHub.
6. Create a Pull Request.
7. Team Lead reviews the Pull Request.
8. After approval, merge into `develop`.
9. After testing, merge `develop` into `main`.

---

## Branch Protection

- Do not commit directly to the `main` branch.
- All changes should go through a Pull Request.
- At least one review is required before merging.
- Resolve merge conflicts before merging.

---

## Branch Naming Convention

- feature/<feature-name>
- bugfix/<bug-name>
- hotfix/<issue-name>
- docs/<document-name>

Examples:
- feature/team-lead
- feature/backend-upload
- feature/frontend-upload
- feature/document-processing
- feature/ai-rag
- feature/database
- feature/devops
- docs/integration-checklist
- docs/branching-strategy
