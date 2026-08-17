# 🤝 Contributing Guidelines

We welcome contributions to Merit AI! Please follow these guidelines to ensure a smooth development and review process.

---

## Code Style & Standards

### Backend (Python)
- Code formatting enforced by **Black** (line length 88).
- Import ordering managed by **isort**.
- Type annotations required for all public methods (**mypy** strict mode).
- Run linting before submitting PR:
  ```bash
  cd backend
  black app tests
  isort app tests
  flake8 app tests
  mypy app tests
  pytest
  ```

### Frontend (TypeScript / Next.js)
- Code style enforced by **ESLint** and **Prettier**.
- Run linting before submitting PR:
  ```bash
  cd frontend
  npm run lint
  ```

---

## Git Workflow & Commit Guidelines

- Use feature branches off `main`: `feature/short-description` or `fix/issue-description`.
- Follow Conventional Commits format:
  - `feat: add PDF text highlight feature`
  - `fix: handle edge case in docx table parser`
  - `docs: update deployment instructions`
  - `test: add unit test for matching policy`
