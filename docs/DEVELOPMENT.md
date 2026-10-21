# Developing Privacy Forge

## Source of truth

Edit Python under `src/`. Copy changed `engine.py`, `lab.py`, `common.py`, and `review.py` to `docs/`. Pipeline Pulse also mirrors `challenges.py`. Keep public API names and repository slugs stable; changing a heading does not require a breaking API rename.

## Validate a change

```bash
python -m unittest discover -s tests -v
python scripts/check_site.py
python scripts/build_preview.py
node --check docs/studio.js
node --check docs/review-desk.js
```

Pipeline Pulse additionally uses `node --test tests/vault.test.cjs`.

After regenerating the sample, run Python tests once more if the preview changed. For UI changes, check keyboard navigation, labels, narrow layouts, priority filters, checklist reset on a new experiment, and export contents. Do not present the synthetic first-visit preview as newly computed input.

## Architecture

`engine.run` routes studio requests through `lab.run`, then `review.attach`. Legacy calls remain unchanged. The browser worker downloads mirrored Python files; the CLI and HTTP server import native files. `review-desk.js` receives `workbench:result` DOM events with the result and preview flag. It renders the report and keeps only inspection checkmarks in memory.

## Release checklist

Update `VERSION` and `CHANGELOG.md`; document observable changes. Regenerate the preview and bump changed browser assets' query versions. Open a PR with the relevant validation output. Wait for checks before merging; GitHub Pages publishes `docs/` from the default branch.
