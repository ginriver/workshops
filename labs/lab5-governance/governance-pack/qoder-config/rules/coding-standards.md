<!-- Recommended rule type: Always Apply -->
# Coding standards

- Layering: `app/routes/` (thin) -> `app/services/` (logic) -> `app/models/` (DB).
  Never place business logic or direct DB queries in `app/routes/`.
- Every API request/response MUST go through a Pydantic schema in `app/schemas/`.
- Every new feature MUST ship with pytest tests in `tests/` (happy path, boundary, error cases).
- Naming: snake_case for functions/variables/modules, PascalCase for classes.
- Error semantics: 404 for missing resources, 409 for duplicates, 422 for validation errors.
- Never hardcode secrets or credentials; use environment variables.
- Comments may be Japanese or English; keep them concise and focused on "why".
