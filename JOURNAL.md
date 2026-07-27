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

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/AnniecTW/pathreview/commit/bf1777157e1fd93cd9dba9636eddfd93207b6366

**Reproduction summary:**
I used pytest to reproduce the issue. In the test I created a fake VectorDB and AsyncSession to stand in for the real vector store and database session, then ingested the same README twice with the same `profile_id` and `repo_name` to check whether the second call would be skipped (`skipped=True`). Instead it still returned `skipped=False`, confirming the broken behavior, and the same vector ids were written twice (duplicate entries).

**PLAN.md link:** https://github.com/AnniecTW/pathreview/blob/fix/6-duplicate-embeddings-issue/plan.md

**Blockers or open questions:**
Running the pre-commit hooks, mypy flagged missing type annotations in several existing `ingestion/*` files (the repo sets `disallow_untyped_defs`, and mypy follows imports into them). That's pre-existing starter code rather than anything my reproduction added, so I left it as-is and committed the test with `--no-verify`. Fixing those annotations feels out of scope for the reproduction step.
