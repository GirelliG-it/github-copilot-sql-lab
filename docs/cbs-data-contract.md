# CBS seaport data contract

## Source
 - Publisher: Statistics Netherlands (CBS).
 - Dataset: 85598NED - Zeevaart; overgeslagen gewicht, zeehaven,
   vervoerstroom, soort lading.
 - URL: https://www.cbs.nl/nl-nl/cijfers/detail/85598NED

## Grain

Each row represents the weight measured for one cargo category, one flow, one port, during one quarter for a specified year. For example, Q1 2023.

## Candidate key

Identifying fields consist of port, flow, cargo category and year-quarter.

## Measurement and unit

- Measure: gross-plus weight of handled cargo.
- Unit: thousand tonnes.

Gross-plus weight includes goods, packaging and, for container or
roll-on/roll-off transport, the empty transport unit.

Multiply the source value by 1000 to convert to tonnes.
