# Privacy Forge — user guide

## Start with the question

Experiment with column transformation policies and inspect remaining identification signals.

## Five-minute tour

Run a synthetic sample → change a column policy → inspect residual signals and group sizes → open Review desk → export the handoff.

1. Open [the live app](https://m-qazi99.github.io/privacy-forge/) and inspect the labeled synthetic preview.
2. Review the editable inputs before selecting **Run experiment**. The first run downloads a pinned Python runtime.
3. Inspect the workspace views; choose a source record, activity or passage when available.
4. Scroll to **Review desk**. Filter **Investigate**, **Review**, or **Context**. Check an item only after inspecting its evidence.
5. Export the reviewed handoff. Its checkmarks describe your inspection state; they are not automatic sign-off.

## Review Desk in this project

Retained-signal priorities, singleton-group prompts, and missing quasi-identifier checks without source cell values in the review report.

Every computed run replaces the priorities and clears the checklist. Switching workspace views retains it. Reload also clears it. Unfiltered exports include every priority and its checked state.

## Downloads and data

The input editor supports local files. Inputs are processed in a Python worker; the initial runtime comes from jsDelivr. Exported full experiments include their inputs. Review Desk exports omit original cell values, but can contain column names, activity names, query text or document titles. Review all exports before sharing.

## Troubleshooting

- **Runtime does not start:** check connectivity to jsDelivr, then retry. Use the native CLI if WebAssembly/CDN access is unavailable.
- **Invalid request:** keep the source error and reduce the input to a synthetic reproducer. Field constraints are in [API.md](API.md).
- **Old results after editing:** select Run experiment again. The current result represents the last submitted request.
- **Checklist disappeared:** it resets for a new result or page reload by design.

## Limits

Heuristic scanning can miss identifiers and flag innocent values. Generalization retains information and does not establish anonymity. Residual signals count detected cells kept or generalized, not re-identification probability. Group-size checks are exploratory, not a full privacy model. Review output before sharing.

Inputs remain in the active tab. Initial runtime files come from jsDelivr and fonts from Google Fonts; no input is sent to these services. Inputs and snapshots are not automatically persisted. Exported experiments include their input; review before sharing. File contents are limited to 2 MB and CSV datasets to 10,000 rows.

[Implementation](ARCHITECTURE.md) · [Report an issue](https://github.com/m-qazi99/privacy-forge/issues/new/choose)
