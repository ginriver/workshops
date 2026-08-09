# AGENTS.md — Team Development Standards (Calibration Tracker)

All AI-assisted changes in this repository MUST follow the team standards below.
Detailed rules live in `.qoder/rules/`, domain knowledge in `.qoder/skills/`,
and deterministic gates in `.qoder/settings.json` (hooks).

## Layering

- `app/routes/` stays thin: request parsing and response shaping only.
- Business logic goes to `app/services/`; DB tables in `app/models/`; Pydantic schemas in `app/schemas/`.

## Quality

- Every new or changed API MUST have Pydantic schemas and pytest tests under `tests/`.
- `python3 -m pytest -q` must pass before work is considered done (enforced by the Stop hook).
- Destructive shell commands (`rm -rf`, `git push --force`, `DROP TABLE`) are forbidden (enforced by the PreToolUse hook).

## API semantics

- All endpoints under `/api/v1`.
- 404 when a resource is missing, 409 on duplicates, 422 on validation errors.

## Domain (metrology)

- Measurement uncertainty follows the GUM approach: Type A / Type B evaluation,
  combined standard uncertainty uc(y), expanded uncertainty U = k * uc(y) with k = 2.
- See `.qoder/skills/uncertainty-eval/SKILL.md`.
