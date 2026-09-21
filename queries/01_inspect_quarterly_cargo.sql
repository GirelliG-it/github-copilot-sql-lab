SELECT *
FROM cargo
WHERE regexp_full_match(Perioden, '^[0-9]{4} [1-4]e kwartaal\*?$');
