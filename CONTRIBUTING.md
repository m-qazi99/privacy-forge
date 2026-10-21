# Contributing

Thanks for helping improve Muzammil Qazi's public data workbench.

## Start with a reproducible problem

Read the README and linked implementation first. Open an issue with the expected behavior, observed behavior, environment and a small synthetic reproducer. Do not include employer data, credentials, personal records or private operational logs. For larger changes, agree the scope in an issue first.

## Development and PRs

1. Fork the repository and create a branch named `fix/short-description`, `feat/short-description` or `docs/short-description`.
2. Keep the change focused and preserve existing public entry points unless a breaking change is explicitly documented.
3. Run the checks below and relevant new tests. Add tests for meaningful policy boundaries rather than mirroring implementation details.
4. Open a PR explaining the concrete before/after behavior, validation, limitations and any screenshot needed to review a UI change.
5. Address review feedback and wait for relevant checks before merging.

```bash
python -m unittest discover -s tests -v
python scripts/check_site.py
```

For the five apps, edit Python under `src/` and keep mirrored browser files in `docs/` byte-identical. Regenerate synthetic previews after analytical changes. Existing licenses continue to apply; do not add third-party assets without their required attribution.

Useful first contributions include clearer examples, reproducible regression cases, accessible labels, and documentation corrections. Contribution counts are a consequence of real work, not a project goal.
