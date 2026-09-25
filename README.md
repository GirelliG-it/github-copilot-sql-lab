# github-copilot-sql-lab

## Purpose

The central research question is: **Can GitHub Copilot be deployed effectively and responsibly for SQL development?**

This project explores writing, explaining, and reviewing SQL with Copilot, checking its suggestions against explicit requirements and executable tests. The focus is on correctness, reliability, security, and human oversight.

Dutch seaport cargo data from CBS StatLine provides the practical case study. We use DuckDB and Python to develop SQL skills, test queries, and record evidence about Copilot’s strengths and limitations.

## v0.1 scope

The proposed v0.1 combines a reproducible analysis of one official Dutch seaport cargo dataset with documented evaluations of Copilot-assisted SQL development. Final scope and release criteria remain to be agreed.

- **Source:** CBS StatLine dataset 85598NED, covering cargo weight by seaport, transport flow and cargo type.
- **Pipeline:** preserve the acquired source data, validate and transform it into analytical tables, and use SQL queries to examine changes over time.
- **Database:** DuckDB for local data storage, transformation and analysis.

## Repository structure

Current locations relevant to the SQL case study and Copilot evaluations are:

- `docs/` — project documentation, including the preserved future research plan.
- `queries/` — SQL queries, including the quarterly cargo filter.
- `tests/` — automated SQL correctness tests using controlled test data.
- `learning-log.md` — learning notes.

Other directories contain material or placeholders from the original learning plan. Their presence does not indicate implemented functionality.

## Analytical question

How have inbound and outbound cargo volumes changed across Dutch seaports since 2015, and which ports and cargo types contributed most to those changes?

The intended user is a government policy analyst identifying ports or cargo categories that warrant further investigation. The analysis will compare matching quarters across years to help distinguish persistent declines from isolated weak quarters.
Cargo volumes alone cannot establish whether changes were caused by geopolitical events or staffing shortages.


## Testing

From the repository root, with the project environment active, run:

```bash
python -s -m pytest -v
```

Python’s `-s` option excludes user-wide Python packages.

The suite currently contains three tests using controlled, in-memory DuckDB data:

- Preserve valid quarterly rows while excluding annual and NULL-period rows.
- Reject an invalid fifth-quarter label.
- Verify quarterly cargo totals, previous totals per port, percentage growth, missing/zero-denominator handling, and output order.

Last recorded validation on 2026-09-22: **3 passed**.

These tests do not validate the complete CBS dataset or source schema. The growth fixture assumes consecutive quarters; missing-quarter behavior remains untested.


## Running the quarterly query

From the repository root, start Python with user-wide packages excluded:

```bash
python -s
```

Then run:

```python
from pathlib import Path
import duckdb

connection = duckdb.connect(":memory:")
connection.execute("""
    CREATE TABLE cargo AS
    SELECT *
    FROM read_csv('data/raw/85598NED_SelectieZonderStatSymbol_20260905202831.csv')
""")
sql = Path("queries/01_inspect_quarterly_cargo.sql").read_text()
connection.sql(sql).show()
connection.close()
```
The CSV must exist at the specified path. It is excluded from Git.

### Acknowledgements

This project was inspired by the R&D department of [ChipSoft](https://www.chipsoft.com/nl-NL)
