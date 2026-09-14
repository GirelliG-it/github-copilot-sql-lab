# github-copilot-sql-lab

## Purpose

The aim of this project is to study and build a production-oriented pipeline focused on ingestion, validation, transformation and SQL analysis. In this case study the main focus will be analysing and processing Dutch seaport cargo volumes from the official CBS StatLine Dataportal. The current status is planning and initial data exploration.

The emphasis is on understanding the relational model, predicting database behavior, designing reliable schemas, and verifying claims with executable SQL.

## v0.1 scope

The first version will turn one official dataset into a reproducible analysis of Dutch seaport cargo trends.

- **Source:** CBS StatLine dataset 85598NED, covering cargo weight by seaport, transport flow and cargo type.
- **Pipeline:** preserve the acquired source data, validate and transform it into analytical tables, and use SQL queries to examine changes over time.
- **Database:** DuckDB for local data storage, transformation and analysis.

## Repository structure

The repository is being reorganised around the v0.1 logistics pipeline. Current locations relevant to this work are:

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

    python -s -m pytest -v

The `-s` option excludes user-wide Python packages.

The current test runs the quarterly SQL query against a small in-memory
dataset. It checks that quarterly rows and their weights are preserved
and annual rows are excluded. It does not yet validate the real CBS
data or the complete source schema.

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
connection.execute(sql).show()
connection.close()
```

The CSV must exist at the specified path. It is excluded from Git.
