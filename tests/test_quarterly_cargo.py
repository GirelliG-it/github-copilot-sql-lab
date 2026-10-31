from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent

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

    sql = (
        PROJECT_ROOT / "queries" / "01_inspect_quarterly_cargo.sql"
    ).read_text(encoding="utf-8")
    actual = connection.execute(sql).fetchall()

    expected = [
            ('2023 1e kwartaal*', 100),
            ('2023 2e kwartaal*', 200),
            ]

    assert sorted(actual) == sorted(expected), (
    f"Expected {expected}, got {actual}"
    )
    connection.close()


def test_quarterly_filter_rejects_invalid_quarter_number():

    connection = duckdb.connect(":memory:")
  
    connection.execute("""
    CREATE TABLE cargo (
        Perioden VARCHAR,
        weight BIGINT
      )
      """)
  
    connection.execute("""
    INSERT INTO cargo VALUES
    ('2023 1e kwartaal', 100),
    ('2023 5e kwartaal', 999)
    """)

    sql = (
        PROJECT_ROOT / "queries" /
        "01_inspect_quarterly_cargo.sql"
    ).read_text(encoding="utf-8")
    actual = connection.execute(sql).fetchall()
 

    expected = [
            ('2023 1e kwartaal', 100),
            ]

    assert sorted(actual) == sorted(expected), (
    f"Expected {expected}, got {actual}"
    )
    connection.close()


