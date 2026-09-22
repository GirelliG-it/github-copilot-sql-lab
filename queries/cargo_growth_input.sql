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
