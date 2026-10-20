<a href="https://m-qazi99.github.io/privacy-forge/"><img src="docs/banner.svg" alt="Privacy Forge — DATA PRIVACY WORKSPACE" width="100%"></a>

**[Open the live app ↗](https://m-qazi99.github.io/privacy-forge/)** · [Python engine](src/engine.py) · [Tests](tests/) · [Example input](examples/sample.json)

Review sensitive-field signals, mask whole cells, and export a sanitized copy. Inspect every flagged field before sharing data.

## What works

- Header-aware detection
- Pattern-based discovery
- Run-scoped tokenization
- Masked CSV export

- Sample inputs, local file uploads, real result tables and charts.
- JSON and Markdown report exports; domain-specific text/CSV exports where applicable.
- Identical dependency-free Python engine in the live browser app, local API, and CLI.

## Run locally

Python 3.10+; no pip packages required for the engine or local server.

```sh
python server.py
# Open http://127.0.0.1:8000
```

The browser UI loads Pyodide from a pinned jsDelivr URL. An internet connection is required for the first runtime load. Alternatively use native Python:

```sh
python src/cli.py < examples/sample.json
python -m unittest discover -s tests -v
python scripts/check_site.py
```

## Local API

```sh
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H 'Content-Type: application/json' \
  --data-binary @examples/sample.json
```

The local API is bound to loopback and is a development server, not a hardened production service. The public site uses a Python WebAssembly worker instead of a backend server.

## Architecture

| Layer | Implementation |
| --- | --- |
| Python analysis | `src/engine.py` and `src/common.py`, standard library only |
| Public browser execution | Pyodide 0.27.7, pinned CDN, dedicated Web Worker |
| Interface | Semantic HTML, responsive CSS, vanilla JavaScript, text-safe rendering |
| Local API | Python `http.server`, `POST /api/analyze` |
| Deployment | GitHub Pages from `main` / `docs` |
| Validation | Unit tests, sample CLI, native/browser engine parity check, GitHub Actions |

## Input contract and limitations

Heuristic detection can miss sensitive data and flag harmless values. This is a review tool, not a compliance or anonymization guarantee.

CSV/text inputs are capped at 2 MB. CSV engines allow up to 10,000 rows; result tables show the first 200 rows, while exports include all results. Browser analysis can be cancelled by terminating its worker. The public app sends no input to an analysis server; runtime files are fetched from jsDelivr and application files from GitHub Pages. No analytics, accounts, or telemetry are included.

Privacy-sensitive uploads should still be reviewed for your organization's data-handling requirements. Avoid putting private datasets into the public repository.

## Reuse and deployment

Publish the `docs` directory with GitHub Pages. Keep `docs/engine.py` and `docs/common.py` synchronized with `src/` after engine changes; the site check fails when they differ. Update the canonical URL and links if deploying under another account.

## About

An independent portfolio project by [Muzammil Qazi](https://m-qazi99.github.io/), created in October 2026 with AI-assisted implementation and human-directed review. It is not an employer deliverable, evidence of production adoption, or a claim of measured business impact.

[MIT license](LICENSE) · [Pyodide documentation](https://pyodide.org/en/stable/usage/index.html)
