# SQL and DDL Learning Path

## Purpose

This path develops production-grade SQL proficiency and then applies it to a concrete R&D goal: evaluating whether an AI coding assistant such as GitHub Copilot can be used effectively and responsibly for SQL development against real organizational data models.

The emphasis is on understanding the relational model, predicting database behavior, designing reliable schemas, and verifying claims with executable SQL. The research phase then adds experimental design, repeatable AI evaluations, safety analysis, IDE comparison, and evidence-based recommendations.

## North-star capability

The destination is not merely “can write SQL” or “can prompt Copilot.” You should be able to answer this kind of question with defensible evidence:

> Under which tasks, schema-context conditions, tools, and safeguards does an AI assistant improve SQL development—and where does it introduce unacceptable correctness, security, performance, or consistency risks?

That requires two connected kinds of competence:

| Competence | Demonstration |
| --- | --- |
| SQL judgment | Independently recognize correct semantics, missing constraints, unsafe writes, cardinality errors, non-idempotent operations, poor plans, and dialect mistakes. |
| Research judgment | Design representative tasks, control variables, define scoring rules before testing, repeat trials, distinguish observation from inference, and communicate limitations. |
| AI-output evaluation | Test generated SQL rather than accepting plausible text; assess correctness, safety, consistency, maintainability, and performance separately. |
| Data-model communication | Supply enough schema context for a task without exposing unnecessary or sensitive information, and determine how context quality changes output quality. |
| Organizational adoption | Translate findings into IDE guidance, review controls, best practices, documentation, training exercises, and a bounded rollout recommendation. |

## Curriculum architecture

The path has two layers:

1. **Modules 0–12 — SQL authority:** become capable of judging AI output without depending on the AI to tell you whether its own work is correct.
2. **Modules 13–18 — AI-assisted SQL research:** build and run a reproducible evaluation that resembles the proposed R&D assignment.

### Dialect strategy

- ANSI SQL is being used as the conceptual baseline.
- PostgreSQL is used for transactional behavior, privileges, concurrency, and plan analysis.
- DuckDB is used for analytical execution and portable local experiments.
- A **SQL Server bridge** is being added for representative tasks.
- Keep dialect-specific files separate whenever a supposedly portable version would hide meaningful behavior.

## Repository structure

```text
sql-open-data-lab/
├── README.md
├── migrations/
│   ├── postgres/
│   ├── duckdb/
│   └── sqlserver/
├── seeds/
├── queries/
├── exercises/
├── tests/
├── explain/
├── research/
│   ├── protocol/
│   ├── tasks/
│   ├── prompts/
│   ├── raw-results/
│   ├── scored-results/
│   └── analysis/
├── training-material/
└── learning-log.md
```

## Running domain model

| Concept | Meaning |
| --- | --- |
| Catalog | An open-data publisher or API, such as a CKAN portal |
| Resource | A discoverable file or API endpoint belonging to a catalog |
| Inspection | One attempt to determine format, accessibility, and queryability |
| Authorization | An explicit decision permitting a particular resource to be loaded |
| Load attempt | The outcome of one authorized persistence attempt |

### Mechanisms

Declarative SQL, candidate keys, three-valued logic, logical query processing order, and transaction boundaries.

### Final research deliverables

- Research plan and versioned protocol.
- Reproducible benchmark and anonymized/synthetic schema packages.
- Raw and scored results with an audit trail.
- Quality, safety, reliability, consistency, and productivity analysis.
- IDE/workflow comparison.
- Best-practice and governance guide.
- Hands-on training module.
- Technical report and management presentation.
- Recommendation: adopt, adopt with constraints, run a further pilot, or do not adopt for specified task classes.

### Why this matters in R&D

The useful result is not “Copilot is good” or “Copilot is risky.” It is a bounded map of where it helps, which evidence supports that claim, and which controls must accompany each use case.
