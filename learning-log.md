## 2026-09-22 — Quarterly cargo growth and Copilot evaluation

Built a DuckDB query that aggregates cargo categories into quarterly totals per port, retrieves previous totals with `LAG()`, and calculates percentage growth.

### What I learned

- CTEs give intermediate query results names within one SQL statement.
- `GROUP BY` combines rows; window functions add information without collapsing the resulting rows.
- `PARTITION BY port` gives each port its own history.
- `LAG()` retrieves the previous available row, which is only the previous calendar quarter when quarters are consecutive.
- `CASE` returns NULL growth when the previous total is missing or zero.

### Testing and debugging

The growth test checks six expected output rows, including positive and negative growth, independent port histories, and zero-denominator handling.

A passing test is not sufficient evidence if its assertion is missing. Restoring `assert actual == expected` verifies both the returned values and their order.

Relative SQL paths require running the current tests from the repository root.

Final full-suite result: 3 passed in 0.08s.

### Copilot evaluation

The first review request accidentally omitted the SQL. Copilot acknowledged the missing context instead of claiming to have reviewed the implementation.

After receiving the query, Copilot assessed it as meeting the stated requirements. Its main assessment agreed with the tested examples, but it introduced an unsupported uniqueness assumption and reversed the missing-quarter explanation in its final paragraph.

The complete evidence is recorded in [Evaluation 03](docs/copilot-evaluation-03.md).

### Remaining scope

The query uses synthetic data and assumes consecutive quarters. Missing quarters, duplicate records, and integration with the real CBS dataset remain unverified.
