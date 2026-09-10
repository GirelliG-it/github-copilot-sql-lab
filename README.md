# Fundamentals of Data Engineering Project

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
- `queries/` — reserved for analytical SQL queries.
- `tests/` — reserved for data-quality and software tests.
- `learning-log.md` — learning notes.
- `AGENTS.md` — mentoring and collaboration instructions.

Other directories contain material or placeholders from the original learning plan. Their presence does not indicate implemented functionality.

## Analytical question

How have inbound and outbound cargo volumes changed across Dutch seaports since 2015, and which ports and cargo types contributed most to those changes?

The intended user is a government policy analyst identifying ports or cargo categories that warrant further investigation. The analysis will compare matching quarters across years to help distinguish persistent declines from isolated weak quarters.

Cargo volumes alone cannot establish whether changes were caused by geopolitical events or staffing shortages.
