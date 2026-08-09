<!-- Recommended rule type: Specific Files (app/routes/*.py) -->
# API design rules

- Prefix all routers with `/api/v1`.
- Return Pydantic response models; never return raw ORM objects.
- HTTP status semantics: 201 on creation, 404 for missing resources,
  409 for duplicates, 422 for validation errors.
- List endpoints return newest-first and may accept an `instrument_id` filter.
- Route functions MUST delegate to `app/services/`; no direct DB queries in routes.
