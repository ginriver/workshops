---
description: Review uncommitted changes against the team development standards
---

Review the uncommitted changes (`git diff HEAD`) against the team standards and output a compliance report:

1. Layering: is there business logic or direct DB access in `app/routes/`?
2. Schemas: is there a new/changed API without a Pydantic schema in `app/schemas/`?
3. Tests: is there a feature change without pytest coverage in `tests/`?
4. API semantics: `/api/v1` prefix and correct 404/409/422 usage?
5. Safety: any destructive commands or hardcoded secrets in the diff?

Output a table with PASS / VIOLATION per check (with file references) and an overall verdict.
