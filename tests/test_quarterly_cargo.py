from pathlib import Path
import duckdb

def test_quarterly_filter_excludes_annual_rows():
    connection = duckdb.connect(":memory:")

    connection.execute("""
    CREATE TABLE cargo (
    Perioden VARCHAR,
    weight BIGINT
    )
    """)

    connection.execute("""
    INSERT INTO cargo VALUES
    ('2023*', 300),
    ('2023 1e kwartaal*', 100),
    ('2023 2e kwartaal*', 200),
    (NULL, 999)
    """)

    sql = Path("queries/01_inspect_quarterly_cargo.sql").read_text()
    actual = connection.execute(sql).fetchall()

    expected = [
            ('2023 1e kwartaal*', 100),
            ('2023 2e kwartaal*', 200),
            ]

    assert sorted(actual) == sorted(expected), (
    f"Expected {expected}, got {actual}"
    )

    connection.close()
