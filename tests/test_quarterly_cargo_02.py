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




