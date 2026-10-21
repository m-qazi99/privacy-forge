# Privacy Forge: engineering notes

## Product decision

The product is an investigation workspace rather than an input/report landing page. Each view answers a distinct question; controls change the actual Python model. Synthetic presets provide reproducible demonstrations without claiming enterprise telemetry.

## Computation

A column policy selects auto, keep, redact, tokenize, generalize, or drop. Pattern/header signals identify candidates. Tokens use a random per-run salt; numeric generalization uses decade buckets. Exact equivalence groups over selected transformed quasi-identifiers expose small groups. A receipt hashes input and output without storing original values or the salt.

## Runtime boundary

The public demo is static GitHub Pages with Pyodide 0.27.7. A worker loads `common.py`, `engine.py`, and `lab.py`; it receives a JSON request and returns a JSON-compatible result. All analysis is Python. DOM interaction and charts are JavaScript/SVG. Python startup has a 90-second timeout; each analysis has a 30-second timeout and a stop control. Terminating the worker releases the computation. Native CLI and API entry points use the same engine without WebAssembly.

## State and data

Inputs are editable and stay in the tab. Successful exports bind to the input submitted for that run, rather than a subsequently edited form. Experiment snapshots retain summary metrics in memory, with a maximum of four. Reload clears snapshots. There are no analytics, server uploads, external model calls, or automatic input persistence. Exporting an experiment includes its input and must be reviewed before sharing.

## Accessibility and display

Semantic buttons, form labels, visible focus, keyboard-accessible tabs, a skip link, reduced-motion support, and responsive layouts are included. Pipeline nodes can be selected with Enter/Space as well as pointer clicks. Narrow pipeline canvases scroll horizontally so activity labels remain readable. Charts are accompanied by evidence or textual summaries. Light themes preserve the portfolio's pearl/champagne direction.

## Tradeoffs and limitations

Heuristic scanning can miss identifiers and flag innocent values. Generalization retains information and does not establish anonymity. Residual signals count detected cells kept or generalized, not re-identification probability. Group-size checks are exploratory, not a full privacy model. Review output before sharing.

## Validation

The repository tests both the original and advanced engine, serialization, algorithm boundaries, and invalid requests. `scripts/check_site.py` checks browser/native Python parity and deployable assets. Tests are run through GitHub Actions on every push. Browser interaction validation is recorded in the delivery notes rather than represented as automated end-to-end CI.

## First-visit preview

`sample-result.js` contains the native Python result for the synthetic studio sample, generated at build time. The UI labels it Synthetic preview until the visitor runs the worker. Exports and snapshots enable only after an actual Python run. This provides a useful first visit without pretending a browser computation has already happened.


## Version 2.1 review-to-handoff layer

`engine.run` preserves legacy requests. Studio requests run the existing analysis, then `review.attach` derives deterministic priorities from the computed result. The review layer does not modify inputs or perform remediation. The mirrored `review.py` is downloaded by the browser worker and checked for native/browser parity.

`review-desk.js` listens for `workbench:result`, renders Python priorities, filters by severity and retains inspection checks in memory. New results and page reloads clear those checks. Python exports unchecked Markdown and JSON; the UI exports Markdown with the visitor's checkmarks. A checked item is not approval or certification. See [API](API.md), [user guide](USER_GUIDE.md), and [development workflow](DEVELOPMENT.md).
