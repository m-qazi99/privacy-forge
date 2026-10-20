<p align="center"><a href="https://m-qazi99.github.io/privacy-forge/"><img src="docs/banner.svg" alt="Privacy Forge Studio — An inspectable privacy transformation experiment." width="100%"></a></p>
<p align="center"><a href="https://m-qazi99.github.io/privacy-forge/"><strong>Launch the interactive studio ↗</strong></a> · <a href="#run-locally">Run Python locally</a> · <a href="docs/ARCHITECTURE.md">Architecture</a> · <a href="tests/test_studio.py">Tests</a></p>
<p align="center"><img src="https://github.com/m-qazi99/privacy-forge/actions/workflows/tests.yml/badge.svg" alt="Python engine checks"> <img src="https://img.shields.io/badge/Python-3.11%2B-477a62?style=flat-square" alt="Python 3.11+"> <img src="https://img.shields.io/badge/License-MIT-bb985b?style=flat-square" alt="MIT license"></p>

# Privacy Forge Studio

**An inspectable privacy transformation experiment.**

Design a column-by-column transformation policy. Explore what stays useful, what remains exposed, and how small groups can reveal more than expected.

## Explore the product

Run **Balanced policy** → change a field transformation → apply → inspect **Output preview** → compare **Group exposure** → try **Retain detected fields** to see residual signals rise.

| Capability | What you can inspect |
|---|---|
| Visual column policy builder | Python-computed results, accessible controls, and exportable evidence |
| Six transformation actions | Python-computed results, accessible controls, and exportable evidence |
| Quasi-identifier group exposure | Python-computed results, accessible controls, and exportable evidence |
| Hashed input/output audit receipts | Python-computed results, accessible controls, and exportable evidence |

The interface includes three synthetic scenarios, four workspace views, light multicolor themes, editable inputs, local file loading, in-memory experiment snapshots, keyboard shortcuts, and downloadable artifacts. The **input editor** exposes the real experiment rather than hiding the model behind a decorative dashboard.

## Python mechanics

A column policy selects auto, keep, redact, tokenize, generalize, or drop. Pattern/header signals identify candidates. Tokens use a random per-run salt; numeric generalization uses decade buckets. Exact equivalence groups over selected transformed quasi-identifiers expose small groups. A receipt hashes input and output without storing original values or the salt.

## Run locally

No Python packages are required. Use Python 3.11 or newer.

```bash
git clone https://github.com/m-qazi99/privacy-forge.git
cd privacy-forge
python server.py
```

Open **http://127.0.0.1:8000**. The local server exposes the native Python API; the web UI uses the browser worker so its behavior matches the public demo. The public site requires a modern browser with WebAssembly and access to the runtime CDN.

```bash
# Native Python CLI: no browser, CDN, or third-party packages
python src/cli.py < examples/studio.json

# Native Python HTTP API
curl -s http://127.0.0.1:8000/api/analyze \
  -H 'Content-Type: application/json' \
  --data-binary @examples/studio.json

# Engine, boundary, and regression tests
python -m unittest discover -s tests -v
python scripts/check_site.py
```

`examples/studio.json` is the complete version-2 experiment request. The `workspace: "studio"` field selects the advanced engine in `src/lab.py`. The original version-1 API remains available through `examples/sample.json` for compatibility. Errors return HTTP 400 with an `error` message; successful requests return metrics, evidence, artifacts, and a structured `lab` object for visualization.

## Architecture

```mermaid
flowchart TD
    I["Editable inputs and controls"] --> W["Background Python worker"]
    W --> E["engine.py → lab.py"]
    E --> V["Interactive investigation views"]
    E --> X["Evidence and artifacts"]
    A["Native CLI or local HTTP API"] --> E
```

- `src/lab.py` — the advanced, dependency-free Python computation.
- `src/engine.py` — explicit version routing and original API compatibility.
- `docs/lab.py`, `docs/engine.py`, `docs/common.py` — byte-identical browser copies, checked by CI.
- `docs/studio.js` — rendering, interaction, worker lifecycle; no duplicate analytical algorithm.
- `docs/worker.js` — pinned Pyodide 0.27.7 runtime in a Web Worker.
- `tests/` — **22 automated tests**, including scenario boundaries and regressions.
- `.github/workflows/tests.yml` — tests and browser/native source parity on each push.

## Scope and limitations

Heuristic scanning can miss identifiers and flag innocent values. Generalization retains information and does not establish anonymity. Residual signals count detected cells kept or generalized, not re-identification probability. Group-size checks are exploratory, not a full privacy model. Review output before sharing.

Inputs remain in the active tab. Initial runtime files come from jsDelivr and fonts from Google Fonts; no input is sent to these services. Inputs and snapshots are not automatically persisted. Exported experiments include their input; review before sharing. File contents are limited to 2 MB and CSV datasets to 10,000 rows.

## Design and research

This studio is an independent implementation by **Muzammil Qazi**, developed with Codex assistance as a portfolio engineering project. Synthetic scenarios demonstrate the algorithms; they are not employer deliverables or evidence of production adoption. See [design decisions](docs/ARCHITECTURE.md) and [research references](docs/RESEARCH.md).

[Portfolio](https://m-qazi99.github.io/) · [GitHub](https://github.com/m-qazi99) · [MIT](LICENSE)
