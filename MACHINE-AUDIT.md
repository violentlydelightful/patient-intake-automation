# Machine Self-Sufficiency Audit (2026-06-16)

## Self-sufficient on this box? -> With caveats

## Issues found
- **Deps missing:** Python Flask app (`requirements.txt`, `run.py`) with no
  `.venv/`. Needs `python -m venv .venv && pip install -r requirements.txt`
  before it will run. Not installed this pass per audit scope.
- No Mac-only paths or mechanisms found. Fully portable code.
- Secrets are env-driven with safe local fallbacks: `config.py` reads
  `SECRET_KEY` and `DATABASE_URL` from env, defaulting to a dev secret and a
  local SQLite file (`intake.db`). No external secret store dependency.

## Fixed this pass
- None needed.

## Outstanding (needs Brad)
- Create venv + install deps to run locally (`python run.py`, serves :5100).
- Set a real `SECRET_KEY` env var for any non-dev use.

## Resilience (good)
- Git repo, remote `github.com/violentlydelightful/patient-intake-automation.git`,
  clean tree, all pushed.
- No committed secrets; `.gitignore` covers `.env`.
