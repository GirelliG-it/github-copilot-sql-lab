# Evaluation 01 — Quarterly SQL filter

## Research question

Can GitHub Copilot accurately assess the quarterly cargo filter and identify relevant edge cases?

## Setup

- Review date: 2026-09-18
- Validation date: 2026-09-19
- Interface: GitHub.com repository chat
- Plan: Copilot Free
- Model selection: Auto
- Optimization: Balanced
- Query: queries/01_inspect_quarterly_cargo.sql
- Database: DuckDB
- Validation environment: CentOS Stream 10, Python 3.12.13, pytest 9.1.1

## Initial assessment

Copilot assessed the query as adequate when the source uses consistent quarterly labels containing lowercase `kwartaal`.

It predicted that rows with a NULL period would be excluded. It also suggested other possible edge cases, which have not yet been tested.

Copilot reported consulting only the query file and not inspecting tests or executing code. This access boundary was requested but not independently verified.

## Independent validation

The existing test passed before modification.

I added `(NULL, 999)` to the SQL input fixture and left the expected results unchanged. The modified test passed: 1 passed.

The test checks that the two quarterly rows and their weights are returned, while the annual row and the added NULL-period row are excluded.

## Finding and limitations

The result supports Copilot’s prediction about NULL-period exclusion for this fixture.

It does not validate the real CBS CSV, the other suggested edge cases, or Copilot’s overall SQL assessment accuracy. This is one initial evaluation case.

## Test output

> python -s -m pytest -v           
===================================================== test session starts =====================================================
platform linux -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /home/ggirelli/miniconda3/envs/github-copilot-sql-lab/bin/python
cachedir: .pytest_cache
rootdir: /home/ggirelli/Documents/projects/data-engineering-projects/github-copilot-sql-lab
configfile: pyproject.toml
collected 1 item                                                                                                              

tests/test_quarterly_cargo.py::test_quarterly_filter_excludes_annual_rows PASSED                                        [100%]

====================================================== 1 passed in 0.05s ======================================================

## Original prompt

Review queries/01_inspect_quarterly_cargo.sql in this repository.

The query runs in DuckDB. Its intended behavior is to return quarterly cargo rows, exclude annual rows, and preserve all columns and source values for the returned rows.

Assess the query without changing files or executing code. For this initial review, do not inspect the tests.

1. Explain what the query does.
2. Assess whether it meets the intended behavior.
3. Identify assumptions, potential failure cases, and anything you cannot establish from the available evidence.
4. Suggest small test cases that could verify your assessment.

List the files you consulted and distinguish verified facts from assumptions.

## Original Copilot response

## Review summary

The query is:

```sql name=queries/01_inspect_quarterly_cargo.sql url=https://github.com/GirelliG-it/github-copilot-sql-lab/blob/67387b09ccb2ba294a73cb25d2aa42a38e6a22cc/queries/01_inspect_quarterly_cargo.sql#L1-L3
SELECT *
FROM cargo
WHERE Perioden LIKE '%kwartaal%';
```

### 1. What it does

It:

1. Reads from the `cargo` relation.
2. Returns every column using `SELECT *`.
3. Keeps rows where `Perioden` contains the lowercase substring `kwartaal` anywhere in the value.
4. Excludes rows where the predicate evaluates to false or `NULL`.

### 2. Does it meet the intended behavior?

**Partially, subject to the source data conventions.**

- **Returns quarterly rows:** It does so if quarterly values in `Perioden` consistently contain the lowercase text `kwartaal`.
- **Excludes annual rows:** It does so if annual values never contain `kwartaal`. This is not explicitly enforced by the query; it follows indirectly from the text-matching convention.
- **Preserves all columns:** Yes, `SELECT *` requests all columns from `cargo`.
- **Preserves source values:** The query does not transform selected values, so returned values should be unchanged. However, this cannot establish whether `cargo` is a base table, view, or relation with computed columns.

The query is therefore adequate for a simple, known label convention, but it does not robustly model “quarterly” versus “annual” as separate semantic categories.

### 3. Assumptions, failure cases, and unknowns

#### Verified facts

- The query reads from `cargo`.
- It selects all columns.
- It filters on `Perioden`.
- The filter is `LIKE '%kwartaal%'`, requiring the substring `kwartaal`.
- No explicit annual-row predicate is present.
- No columns are renamed, cast, aggregated, or otherwise transformed.
- No tests were inspected and no code was executed.

#### Assumptions

- `Perioden` exists and is text-compatible with `LIKE`.
- Quarterly records use values such as `kwartaal 1`, `kwartaal 2`, etc.
- Annual records use a label that does not also contain `kwartaal`.
- Matching is intended to be case-sensitive or the source data has consistent casing.
- The relation named `cargo` exposes the source columns expected by the requirement.

#### Potential failure cases

- **Case mismatch:** Values such as `Kwartaal 1` or `KWARTAAL 1` may not match. DuckDB `LIKE` matching should not be assumed to be case-insensitive.
- **False positives:** Any non-quarterly value containing `kwartaal` will be included, such as a descriptive or malformed value.
- **Missing values:** Rows with `Perioden IS NULL` are excluded because the predicate evaluates to `NULL`.
- **Unexpected annual labels:** If an annual value contains `kwartaal` in a description, it will be included.
- **Other quarterly representations:** Values such as `Q1`, `2024-Q1`, or numeric quarter codes are excluded.
- **Whitespace or formatting variations:** The query depends on the substring being present exactly as expected; unusual spelling, spacing, or encoding may cause misses.
- **Schema evolution:** `SELECT *` preserves all currently exposed columns, but its output shape can change when the underlying relation changes.
- **Relation semantics:** Without inspecting the definition of `cargo`, it cannot be established whether the values are directly sourced or already transformed by a view.

The available evidence does not establish the actual contents, casing, nullability, schema, or definition of `cargo`, so the query’s correctness against real data cannot be proven from this file alone.

### 4. Suggested small test cases

These could be tested with a small temporary `cargo` fixture, without relying on the repository’s existing tests:

| `Perioden` value | Expected result |
|---|---|
| `kwartaal 1` | Included |
| `kwartaal 4` | Included |
| `jaar 2024` | Excluded |
| `annual 2024` | Excluded |
| `NULL` | Excluded |
| `Kwartaal 1` | Verify intended case behavior; likely excluded with ordinary `LIKE` |
| `Q1` | Excluded unless the query is intended to support this format |
| `not a kwartaal record` | Verify whether substring matching creates an undesired false positive |
| An annual description containing `kwartaal` | Should be excluded if annual exclusion is semantic rather than text-based; this would expose a weakness |

For preservation, include multiple columns with distinctive values and verify that the returned rows contain the same values and column set as the input. Also test a row with `Perioden = 'kwartaal 1'` and another with `Perioden = NULL` to confirm filtering behavior.

## Files consulted

- [`queries/01_inspect_quarterly_cargo.sql`](https://github.com/GirelliG-it/github-copilot-sql-lab/blob/67387b09ccb2ba294a73cb25d2aa42a38e6a22cc/queries/01_inspect_quarterly_cargo.sql#L1-L3)

No tests or other repository files were inspected.
