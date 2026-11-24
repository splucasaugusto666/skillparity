# Aggregate JSON reports (unreleased)

Use `python skillparity.py demo --summary-json` from this development checkout. The current v1.0.0 wheel does not include this option.

```json
{
  "counts": {"DRIFT": 2},
  "exit_code": 1,
  "schema_version": 1,
  "skills": 1,
  "targets": 2
}
```

Aggregate reports contain counts only; they omit skill names, paths, root labels and error details. Counts refer to target cells, not unique skills, and absent statuses are omitted. Exit status includes baseline failures, even though the baseline is excluded from counts. Empty catalogs and incomplete comparisons return 2. Counts still reveal aggregate catalog size and may be sensitive. Invalid arguments or fatal input errors may produce no JSON; inspect the process exit code and handle missing output. The demo intentionally exits 1.

This format is intended for agent integrations and dashboards without requiring callers to parse terminal text. It is not an MCP server. Existing detailed JSON and text formats remain unchanged.
