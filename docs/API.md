# Privacy Forge — Python and HTTP API

## Advanced request

Use the complete [studio example](../examples/studio.json). A JSON object with `workspace: "studio"` selects `lab.py` plus the review layer.

| Field | Meaning | UI input kind |
|---|---|---|
| `csv` | Input dataset | csv |
| `policy` | Column transformation policy | json |
| `quasi` | Quasi-identifiers · comma separated | text |

UI input kinds describe the editor; the versioned example is the authoritative request shape. Existing validation in `lab.py` applies. `examples/sample.json` selects the legacy API and does not include Review Desk.

```bash
python src/cli.py < examples/studio.json
python server.py
# In another terminal:
curl http://127.0.0.1:8000/api/analyze -H 'Content-Type: application/json' --data-binary @examples/studio.json
```

The server binds to loopback only. The HTTP endpoint is a local development interface, not an authenticated public service. It limits the JSON body to 4 MB; individual text inputs and CSV row limits are validated by the engine.

## Response

- `metrics`, `table`, `findings`, `artifacts`: existing report contract.
- `lab`: project-specific analytical evidence used by the workspace.
- `review.version`: `2.1.0`.
- `review.project`, `review.name`: stable slug and display name.
- `review.items[]`: `id`, `severity` (`high`, `review`, `info`), `title`, `detail`.
- `review.summary`: counts by severity; these are not risk or confidence scores.
- `review.scope`: limitations of the review aid.

The two new artifacts are `review-handoff.md` (unchecked Python priorities) and `review-priorities.json`. The UI separately exports `reviewed-handoff.md` with your in-memory checkmarks.

Success: HTTP 200 and JSON. Invalid requests: HTTP 400 with `error`; CLI errors go to stderr with exit code 1. Browser worker errors appear in the workspace. No review item executes a change.

[Source](../src/engine.py) · [Review implementation](../src/review.py) · [Boundary tests](../tests/test_review.py)
