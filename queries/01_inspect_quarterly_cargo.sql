SELECT *
FROM read_csv('data/raw/85598NED_SelectieZonderStatSymbol_20260905202831.csv')
WHERE Perioden LIKE '%kwartaal%';
