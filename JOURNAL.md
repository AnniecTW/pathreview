## Week 7 — Issue selection

**Issue link:** [Issue Link](https://github.com/ascherj/pathreview/issues/6)

**Issue title:** Duplicate embeddings generated when re-ingesting the same repository

**Tier:** Tier 2

**Problem summary:**

The `pipeline.py` doesn't check whether the file has already been ingested, so when a Github repo is re-ingested, the pipeline generates the same vector entries repeatedly. This issue might inflate the scores of the repeated chunks.

A successful fix would avoid ingestion when a repeated file is detected, signal the situation, and simply return the existing result.

Affected files:
`ingestion/pipeline.py`
`core/models/ingested_source.py`

**Selection notes:**
This isn't my first open-source contribution, so I’m choosing Tier 2 for a better fit. I am comfortable tracing how multiple modules interact in the codebase. I’ve found the relevant code/file and understand the surrounding code well enough.

**Branch name:** fix/6-duplicate-embeddings-issue

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
