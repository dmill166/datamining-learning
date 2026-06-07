---
title: datamining-learning Repo Rules
id: agents-datamining-learning
version: 1.0.0
status: active
owner: Dakota Hollmann
maintainer: claude-cowork
created: 2026-06-07
updated: 2026-06-07
scope: repo-local — adds to (and inside this repo, overrides) ~/agents/AGENTS.md
changelog:
  - "1.0.0 (2026-06-07): Initial per-repo AGENTS.md — Phase 2 of the AI-first reorg."
---

# datamining-learning — Repo Rules for Agents

Companion repo for Dakota's April 2026 MSU Denver guest lecture (CS 3120 Machine Learning): "Real-World Data Lifecycles: From Nested JSON to ML-Ready Features."

## Layout

```
projects/2026-ingestion-engine/
  src/
    student/           # simple/beginner tier
    enterprise/        # production tier
  tests/               # pytest (includes student-facing tests)
  docs/
  .env.example         # template for local secrets
  LECTURE_NOTES.md
  EDA_REPORT.md
  requirements.txt

archive-msu-2021/      # 28+ legacy course activities — FROZEN, never modify
```

## Conventions

- Active development lives entirely under `projects/2026-ingestion-engine/`.
- API keys and secrets go in `.env` (gitignored) following `.env.example` — never commit them.

## Hazards

1. **Large file — do not touch:** `archive-msu-2021/activity_25_topic_labelling/data/abcnews-date-text.csv` is 59.82 MB, already over GitHub's 50 MB warning threshold. An LFS decision is pending. Never add any file >50 MB to this repo.
2. **`archive-msu-2021/` is frozen.** Never modify, delete, or reorganize any file inside it.
3. Never commit `.env` or any file containing API keys or credentials.

## Commands

Run from `projects/2026-ingestion-engine/`:

```
pip install -r requirements.txt
pytest
```
