# Evaluation 03 — Quarterly cargo growth

## Research question

Can GitHub Copilot assess a DuckDB query that aggregates cargo categories, retrieves the previous total per port, and calculates percentage growth with missing/zero-denominator handling?

## Setup and scope

- Review and final validation date: 2026-09-22.
- Development branch: research/quarterly-cargo-growth.
- Review workflow: GitHub.com Copilot chat; requested configuration Copilot Free, Auto, Balanced. The underlying model identity was not recorded.
- Database: DuckDB; runtime version was not captured in the supplied test output.
- Environment: CentOS Stream 10, Python 3.12.13, pytest 9.1.1.
- Query: queries/02_quarterly_cargo_growth.sql.
- Synthetic data setup: queries/cargo_growth_input.sql.
- Automated test: tests/test_quarterly_cargo_02.py.
- Assumptions: non-negative, non-NULL weights, non-overlapping categories, consistent units, and consecutive calendar quarters per port.

The SQL and test were developed with assistant guidance and manually entered by the learner. Copilot reviewed the implementation; it did not generate it. This is an exploratory learning case, not a controlled benchmark or an overall accuracy estimate.

## Review sequence

1. The first request omitted the SQL. Copilot explicitly identified the missing query and limited its answer to the specification. This attempt is not counted as an implementation review.
2. The complete SQL was supplied in a follow-up in the same chat. Copilot then assessed it as consistent with the stated requirements under the assumptions.
3. Test results were not part of the supplied review prompts. Copilot was asked not to execute code or inspect repository files and described its answer as static reasoning. Its access boundary was not independently verified.

The prompt copies below reproduce the messages prepared in the learning conversation; the complete outbound chat was not independently exported. Both responses were supplied as text attachments and are preserved below without rewriting their claims.

## Execution evidence

The growth fixture has eight input rows: six from the setup file, plus two Testport rows inserted by the test. Aggregation produces these six expected results:

| Port | Quarter start | Total weight | Previous weight | Growth percent |
|---|---|---:|---:|---:|
| Amsterdam | 2023-01-01 | 50 | NULL | NULL |
| Amsterdam | 2023-04-01 | 40 | 50 | -20.0 |
| Rotterdam | 2023-01-01 | 100 | NULL | NULL |
| Rotterdam | 2023-04-01 | 120 | 100 | 20.0 |
| Testport | 2023-01-01 | 0 | NULL | NULL |
| Testport | 2023-04-01 | 25 | 0 | NULL |

The final saved growth test contains `assert actual == expected`. It checks values, row count, and row order together. The learner ran the full suite from the repository root and supplied the following result:

```text
python -s -m pytest -v

tests/test_quarterly_cargo.py::test_quarterly_filter_excludes_annual_rows PASSED
tests/test_quarterly_cargo.py::test_quarterly_filter_rejects_invalid_quarter_number PASSED
tests/test_quarterly_cargo_02.py::test_quarterly_cargo_growth PASSED

3 passed in 0.08s
```

This is an excerpt of the supplied terminal output. The assistant inspected the saved assertion; the assistant did not independently rerun the suite.

Earlier, the growth test temporarily lacked an assertion. Those passing runs showed that execution completed, but did not verify the expected results. A later run from the tests directory failed to resolve relative SQL paths. Final validation followed restoration of the assertion and execution from the repository root.

## Assessment of Copilot's review

| Claim | Evidence or qualification |
|---|---|
| Categories are aggregated into one total per port and quarter | Supported by Rotterdam's two-category fixture and exact expected totals. |
| Previous totals remain within the same port | Supported by separate first-row NULLs and the expected previous totals. |
| Positive and negative percentage changes are calculated | Supported by Rotterdam +20% and Amsterdam -20%. |
| Missing and zero previous totals produce NULL growth | Supported by the first rows and Testport's second row. |
| Output is ordered by port and quarter | Supported for the fixture by direct list comparison without sorting. |
| LAG uses the previous available row if a quarter is missing | Correctly explained in the main response, but not tested in this case. |

Two weaknesses remain in the review:

- Copilot treats freedom from duplicate source rows as established by our assumptions. Non-overlapping categories do not establish uniqueness of source records. Duplicate handling remains an unspecified data-contract issue.
- The final paragraph reverses the missing-quarter explanation: a gap means the previous available row may no longer represent the previous calendar quarter. The earlier explanation states this correctly.

## Limitations and next questions

- This fixture does not test missing quarters, duplicate source rows, missing port/date values, unchanged totals, a drop from a positive total to zero, large values, or fractional results requiring a floating-point tolerance.
- The dates are synthetic quarter starts. The query does not validate that arbitrary dates fall on quarter boundaries.
- The original CBS CSV is not used in this experiment.
- The full-suite total is three tests, of which one is the growth test. Six expected rows are not six independent test functions.
- The setup uses a temporary table and relative file paths. Run tests from the repository root. Re-executing the setup on the same connection would require addressing the already-existing table.
- The result supports the reviewed behavior for this fixture, not a general claim that Copilot reviews all SQL reliably.

## Query snapshot reviewed

```sql
WITH quarter_totals AS (
  SELECT port, quarter_start, SUM(weight) AS total_weight
  FROM cargo_growth_input
  GROUP BY port, quarter_start
),
with_previous AS (
  SELECT port, quarter_start, total_weight, LAG(total_weight) OVER (
    PARTITION BY port
    ORDER BY quarter_start
  ) AS previous_weight
  FROM quarter_totals
)
SELECT
    port,
    quarter_start,
    total_weight,
    previous_weight,
    CASE
        WHEN previous_weight IS NULL THEN NULL
        WHEN previous_weight = 0 THEN NULL
        ELSE (total_weight - previous_weight)
             / previous_weight * 100.0
    END AS growth_percent
FROM with_previous
ORDER BY port, quarter_start;
```

## Synthetic setup snapshot

```sql
CREATE TEMP TABLE cargo_growth_input (
    port VARCHAR,
    quarter_start DATE,
    cargo_category VARCHAR,
    weight INTEGER
);

INSERT INTO cargo_growth_input VALUES
    ('Rotterdam', '2023-01-01', 'Containers', 60),
    ('Rotterdam', '2023-01-01', 'Bulk', 40),
    ('Rotterdam', '2023-04-01', 'Containers', 90),
    ('Rotterdam', '2023-04-01', 'Bulk', 30),
    ('Amsterdam', '2023-01-01', 'Bulk', 50),
    ('Amsterdam', '2023-04-01', 'Bulk', 40);
```

## Final growth test snapshot

```python
from pathlib import Path
from datetime import date
import duckdb

def test_quarterly_cargo_growth():
    # 1. Create a fresh database and load the six practice rows.
    connection = duckdb.connect(":memory:")
    setup = Path("queries/cargo_growth_input.sql").read_text()
    connection.execute(setup)

    # 2. Add input rows that test growth from zero
    connection.execute("""
    INSERT INTO cargo_growth_input VALUES
        ('Testport', '2023-01-01', 'Bulk', 0),
        ('Testport', '2023-04-01', 'Bulk', 25)
    """)

    # 3. Run the growth query against all the input data.
    sql = Path("queries/02_quarterly_cargo_growth.sql").read_text()
    actual = connection.execute(sql).fetchall()

    # 4. Write down the complete expected answer.
    expected = [
        ('Amsterdam', date(2023, 1, 1), 50, None, None),
        ('Amsterdam', date(2023, 4, 1), 40, 50, -20.0),
        ('Rotterdam', date(2023, 1, 1), 100, None, None),
        ('Rotterdam', date(2023, 4, 1), 120, 100, 20.0),
        ('Testport', date(2023, 1, 1), 0, None, None),
        ('Testport', date(2023, 4, 1), 25, 0, None),
    ]

    assert actual == expected, (
        f"Expected {expected}, got {actual}"
    )

    connection.close()
```

## Attempt 1 — Prompt without SQL

Review the DuckDB SQL above using only this message. Do not inspect repository files, execute code, or propose a replacement query yet.

Input table: cargo_growth_input
- port VARCHAR
- quarter_start DATE
- cargo_category VARCHAR
- weight INTEGER

For this initial exercise, weights are non-negative and non-NULL, categories are non-overlapping, units are consistent, and each port has consecutive calendar quarters.

Requirements:
1. Produce one total per port and quarter by adding category weights.
2. Compare each total with the previous quarter for the same port.
3. Calculate percentage growth as:
   (current total - previous total) / previous total * 100.
4. Return NULL growth when there is no previous total or the previous total is zero.
5. Return results ordered by port and quarter.

Explain how the CTEs, grouping, window function, and CASE expression work together. Assess each requirement and identify any correctness concerns.

Separately explain what would happen if a port had a missing quarter. Distinguish limitations outside the stated assumptions from defects within them.

Suggest small independent test cases. Clearly distinguish reasoning from execution evidence.

## Attempt 1 — Complete Copilot response

I can assess the requirements and the expected reasoning from this message, but no SQL query is included here. Therefore, I cannot verify whether the actual CTEs, `GROUP BY`, window function, or `CASE` expression are implemented correctly. The assessment below is reasoning from the stated specification—not execution evidence.

## Expected query structure

A correct solution would typically use these logical stages:

1. **Aggregation CTE**
   - Groups rows by `port` and `quarter_start`.
   - Sums `weight` across `cargo_category`.
   - Produces one total per port and quarter.

2. **Previous-total CTE or window stage**
   - Applies a window function such as `LAG(total_weight)`.
   - Partitions by `port`, so ports are compared independently.
   - Orders within each partition by `quarter_start`.

3. **Growth calculation**
   - Uses the current total and previous total.
   - Calculates:

     \[
     \frac{\text{current total} - \text{previous total}}
          {\text{previous total}} \times 100
     \]

   - A `CASE` expression should return `NULL` when:
     - there is no previous row/total, or
     - the previous total is zero.
   - Otherwise it should calculate the percentage.

4. **Final ordering**
   - Orders by `port`, then `quarter_start`, both ascending unless otherwise specified.

## Requirement assessment

Because the SQL itself is absent, each item can only be assessed as a correctness criterion:

| Requirement | What the SQL must do | Current assessment |
|---|---|---|
| One total per port and quarter | Group by `port, quarter_start` and sum `weight` across categories | Cannot verify without the query |
| Compare with previous quarter | Use `LAG` over each `port`, ordered by `quarter_start` | Cannot verify without the query |
| Calculate percentage growth | Use the specified numerator, denominator, and multiplication by 100 | Cannot verify without the query |
| Return `NULL` for no previous total or previous total zero | Guard the calculation with a `CASE` expression | Cannot verify without the query |
| Order by port and quarter | Add a final `ORDER BY port, quarter_start` | Cannot verify without the query |

## How the pieces should work together

The aggregation must happen **before** the window function. Otherwise, `LAG` could compare individual category rows rather than the required total for the quarter.

For example, the intended data flow is:

```text
category-level rows
        ↓
GROUP BY port, quarter_start
        ↓
quarterly totals
        ↓
LAG(total) PARTITION BY port ORDER BY quarter_start
        ↓
CASE-based growth calculation
        ↓
ORDER BY port, quarter_start
```

The `LAG` window should operate on the aggregated quarterly result. Its `PARTITION BY port` clause prevents one port’s data from being compared with another port’s data. Its `ORDER BY quarter_start` clause establishes the chronological sequence.

The `CASE` expression must test the previous total before dividing. A condition that only checks whether `LAG` returned `NULL` is insufficient, because a previous total of zero would still cause a division-by-zero problem or an invalid result. The zero check should be applied to the previous total used as the denominator.

## Correctness concerns to check

Even under the stated assumptions, the SQL would have correctness concerns if it does any of the following:

- Groups by `port`, `quarter_start`, and `cargo_category`, leaving multiple rows per quarter.
- Applies `LAG` before category weights are summed.
- Omits `PARTITION BY port`, causing comparisons across ports.
- Orders the window by something other than `quarter_start`.
- Uses `LAG` on raw input rows rather than on one row per port and quarter.
- Divides by the current total instead of the previous total.
- Omits the multiplication by `100`.
- Handles a missing previous row but not a previous total of zero.
- Relies only on a final `ORDER BY` while leaving the window function without its own ordering.
- Uses a non-deterministic ordering where multiple rows remain for the same port and quarter.

Given the assumptions, non-negative and non-NULL weights make the aggregation itself straightforward. Non-overlapping categories and consistent units mean no additional deduplication or unit conversion is required.

## Missing-quarter behavior

A missing quarter is outside the stated assumptions, because the input guarantees consecutive calendar quarters for each port. It is therefore a limitation of the input model rather than a defect within the specified problem.

With a typical `LAG` implementation:

- `LAG` returns the previous **available row**, not necessarily the immediately preceding calendar quarter.
- If a port has rows for Q1 and Q3 but no Q2, Q3 will generally be compared with Q1.
- The result may therefore label the comparison as “previous quarter” even though the elapsed interval is two calendar quarters.
- The percentage calculation itself will still be mathematically valid for the two available observations, but it will not represent quarter-over-quarter growth.

If the business requirement later changes to require strictly adjacent calendar quarters, the query would need additional date-gap detection or a calendar-quarter spine. That is not required under the current assumptions and should not be treated as a defect in this exercise.

## Small independent test cases

These are suggested test inputs and expected behaviors, not execution results.

### 1. First quarter has no previous value

```text
port  quarter_start  category  weight
A     2024-01-01     X         100
A     2024-04-01     X         120
```

Expected:

- Q1 previous total: `NULL`
- Q1 growth: `NULL`
- Q2 previous total: `100`
- Q2 growth: `20%`

### 2. Multiple categories must be added

```text
port  quarter_start  category  weight
A     2024-01-01     X         40
A     2024-01-01     Y         60
A     2024-04-01     X         75
A     2024-04-01     Y         25
```

Expected quarterly totals:

```text
A, 2024-01-01 → 100
A, 2024-04-01 → 100
```

Expected growth for Q2: `0%`.

### 3. Previous total is zero

```text
port  quarter_start  category  weight
A     2024-01-01     X         0
A     2024-04-01     X         50
```

Expected:

- Q1 growth: `NULL`
- Q2 previous total: `0`
- Q2 growth: `NULL`

### 4. Declining total

```text
port  quarter_start  category  weight
A     2024-01-01     X         200
A     2024-04-01     X         150
```

Expected Q2 growth:

```text
(150 - 200) / 200 * 100 = -25%
```

### 5. Multiple ports must remain independent

```text
port  quarter_start  category  weight
A     2024-01-01     X         100
A     2024-04-01     X         120
B     2024-01-01     X         500
B     2024-04-01     X         400
```

Expected:

- A Q2 growth: `20%`
- B Q2 growth: `-20%`
- Neither port should use the other port’s total.

### 6. Missing quarter, outside the assumptions

```text
port  quarter_start  category  weight
A     2024-01-01     X         100
A     2024-07-01     X         130
```

A normal `LAG` over available rows will compare July with January. It will not automatically produce a row for April or recognize that July is not immediately adjacent to January.

## Attempt 2 — Follow-up with SQL

Here is the actual SQL, which was missing from my previous message:

```sql
WITH quarter_totals AS (
  SELECT port, quarter_start, SUM(weight) AS total_weight
  FROM cargo_growth_input
  GROUP BY port, quarter_start
),
with_previous AS (
  SELECT port, quarter_start, total_weight, LAG(total_weight) OVER (
    PARTITION BY port
    ORDER BY quarter_start
  ) AS previous_weight
  FROM quarter_totals
)
SELECT
    port,
    quarter_start,
    total_weight,
    previous_weight,
    CASE
        WHEN previous_weight IS NULL THEN NULL
        WHEN previous_weight = 0 THEN NULL
        ELSE (total_weight - previous_weight)
             / previous_weight * 100.0
    END AS growth_percent
FROM with_previous
ORDER BY port, quarter_start;
```

Please review this implementation against the requirements and assumptions I already supplied.

Do not execute code or inspect repository files. Assess the actual query, distinguish confirmed observations from assumptions, and identify any unmet requirements. Do not propose a replacement query yet.

## Attempt 2 — Complete Copilot response

Direct answer: this SQL is consistent with the stated requirements under the stated assumptions. Based on static review of the SQL alone, I do not see an unmet requirement within those assumptions. I am not claiming execution results; this is a reasoning assessment of the query text.

Confirmed observations from the actual SQL

- The first CTE, `quarter_totals`, does:
  - `GROUP BY port, quarter_start`
  - `SUM(weight) AS total_weight`
  - So it produces exactly one row per port and quarter, which satisfies the “one total per port and quarter” requirement.

- The second CTE, `with_previous`, does:
  - `LAG(total_weight) OVER (PARTITION BY port ORDER BY quarter_start) AS previous_weight`
  - This compares each quarterly total to the prior quarter for the same port, because the window is partitioned by `port` and ordered by `quarter_start`.

- The final `CASE` expression:
  - `WHEN previous_weight IS NULL THEN NULL`
  - `WHEN previous_weight = 0 THEN NULL`
  - `ELSE (total_weight - previous_weight) / previous_weight * 100.0`
  - This matches the requirement to return `NULL` when there is no previous total or when the previous total is zero, and to calculate growth otherwise.

- The final `ORDER BY port, quarter_start` satisfies the output-order requirement.

Requirement-by-requirement assessment

1. Produce one total per port and quarter by adding category weights
- Confirmed by the aggregation in `quarter_totals`.
- `SUM(weight)` is appropriate because the assumptions say categories are non-overlapping, weights are non-negative and non-null, and units are consistent.

2. Compare each total with the previous quarter for the same port
- Confirmed by `LAG(total_weight) OVER (PARTITION BY port ORDER BY quarter_start)`.
- Because the window is partitioned by `port`, each port is evaluated independently.

3. Calculate percentage growth as:
   (current total - previous total) / previous total * 100
- Confirmed by the `ELSE` branch:
  `(total_weight - previous_weight) / previous_weight * 100.0`
- The multiplication by `100.0` ensures a percentage-style value rather than a decimal fraction.

4. Return NULL growth when there is no previous total or the previous total is zero
- Confirmed by the first two `CASE` conditions:
  - `previous_weight IS NULL`
  - `previous_weight = 0`

5. Return results ordered by port and quarter
- Confirmed by `ORDER BY port, quarter_start`.

How the pieces work together

- The CTEs are ordered intentionally:
  - `quarter_totals` collapses the raw rows into one row per `port` + `quarter_start`
  - `with_previous` then computes the prior quarter’s total for the same port using a window function
  - The final `SELECT` applies the growth logic only after the prior value is available

- The `GROUP BY` is essential because it prevents each category from being compared individually. Without that step, `LAG` would compare category-level rows instead of quarterly totals.

- The window function is essential because it derives “previous quarter” without collapsing the result set to a single row. `LAG` can look back one row within the ordered partition.

- The `CASE` expression is the guardrail:
  - it prevents divide-by-zero and missing-data problems
  - it ensures the function returns `NULL` in the invalid denominator cases instead of erroring or producing meaningless values

Assumptions and their effect

Under the assumptions you supplied, I do not see a defect in the query itself:

- weights are non-negative and non-null
- categories are non-overlapping
- units are consistent
- each port has consecutive calendar quarters

These mean:
- summing weights is valid
- there is no need for special handling to reconcile categories or units
- the `LAG` result is aligned with the actual quarterly sequence

Correctness concerns, if any

These are not defects within the stated assumptions, but they matter if assumptions are violated:

- Missing quarter:
  - The query compares the previous available row, not necessarily the immediately preceding calendar quarter.
  - If a port is missing a quarter, `LAG` will still compare Q3 to Q1, which is a valid “previous observed row” comparison but not necessarily a strict “previous quarter” comparison in the calendar sense.

- Zero total:
  - The query returns `NULL` when previous total is zero, which matches the requirement.
  - If the current total were also zero, the expression would also return `NULL` because the denominator is zero if the previous total was zero; if the same quarter had zero total but previous total was non-zero, the formula would produce a negative percentage only if total < previous total, which is mathematically valid.

- Duplicate rows:
  - The query assumes the source data is already valid and not double-counted by the same `port + quarter + category` combination.
  - Under your stated assumptions this is not a concern.

- Missing or invalid dates:
  - The query relies on `ORDER BY quarter_start` to define chronology.
  - If dates were malformed, that would be outside the assumptions and would need a data-quality fix, not a query logic fix.

Distinguishing assumptions from defects

- Within the stated assumptions: no obvious correctness issue.
- Outside the stated assumptions:
  - a missing quarter would create a semantic mismatch between “previous row” and “previous calendar quarter”
  - a data-quality issue such as duplicate rows or inconsistent date handling would require additional validation and is not a defect in the given query under the provided assumptions

Separate note on missing quarters

If a port had a missing quarter, the query would still execute as written, but the meaning of the comparison changes:

- `LAG` uses the previous row in the ordered result set
- it does not infer or generate absent calendar quarters
- so it does not detect the gap unless extra logic is added outside this query

This is a limitation of the logic relative to the “consecutive calendar quarters” assumption, not a bug inside the assumptions themselves. In other words, it is a problem only if the real-world data does not satisfy the assumption that every quarter exists.

Small independent test cases to reason about

These are not execution evidence; they are independent sanity checks for the logic.

1. First quarter has no previous value
- Input:
  - port A, Q1 total = 100
  - port A, Q2 total = 120
- Expected:
  - Q1 growth = NULL
  - Q2 growth = 20.0

2. Previous total is zero
- Input:
  - port A, Q1 total = 0
  - port A, Q2 total = 50
- Expected:
  - Q1 growth = NULL
  - Q2 growth = NULL

3. Multiple categories in same quarter
- Input:
  - port A, Q1: category X = 40, category Y = 60
  - port A, Q2: category X = 75, category Y = 25
- Expected:
  - Q1 total = 100
  - Q2 total = 100
  - Q2 growth = 0.0

4. Declining value
- Input:
  - port A, Q1 total = 200
  - port A, Q2 total = 150
- Expected:
  - Q2 growth = -25.0

5. Multiple ports
- Input:
  - A: Q1=100, Q2=120
  - B: Q1=500, Q2=400
- Expected:
  - A growth = 20.0
  - B growth = -20.0
  - no cross-port comparison

6. Missing quarter outside assumptions
- Input:
  - A: Q1=100
  - A: Q3=130
- Expected:
  - If treated as a plain ordered series, Q3 compares with Q1
  - This is not a defect of the SQL under the assumption of consecutive quarters, but it would be semantically surprising if calendar quarter continuity is required

Bottom line

Within the assumptions you provided, the SQL is a correct implementation of the stated requirements:
- quarterly aggregation
- per-port lag comparison
- percentage growth formula
- null guard for missing/zero previous totals
- ordering by port and quarter

The main caveat is that a missing quarter would change the interpretation of “previous quarter” from “previous row in the ordered data” to “prior calendar quarter.” That is a limitation outside the assumptions, not a defect within them.
