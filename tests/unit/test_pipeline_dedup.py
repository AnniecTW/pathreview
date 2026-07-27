"""Reproduction test for issue #6: duplicate embeddings on re-ingestion.

NOTE: This asserts the BROKEN behavior on purpose.
"""

import pytest

from ingestion.embeddings.provider import MockEmbeddingProvider
from ingestion.pipeline import IngestionPipeline

README = """# My Project

## Overview
This is a sample project that does useful things with data pipelines.
"""


class FakeVectorDB:
    """Records the ids passed to every add() call, like a ChromaDB collection."""

    def __init__(self) -> None:
        self.added_ids: list[str] = []
        self.add_calls = 0

    def add(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        documents: list[str],
    ) -> None:
        self.add_calls += 1
        self.added_ids.extend(ids)


class FakeAsyncSession:
    """Mimics the real core.database AsyncSession, which has no .query()."""

    def query(self, *args: object, **kwargs: object) -> None:
        raise AttributeError("'AsyncSession' object has no attribute 'query'")


@pytest.mark.unit
class TestIngestionPipelineDeduplication:
    """Reproduces the duplicate-embeddings bug at the pipeline level."""

    @pytest.fixture
    def vector_db(self) -> FakeVectorDB:
        return FakeVectorDB()

    @pytest.fixture
    def pipeline(self, vector_db: FakeVectorDB) -> IngestionPipeline:
        return IngestionPipeline(
            vector_db=vector_db,
            db_session=FakeAsyncSession(),
            embedding_provider=MockEmbeddingProvider(),
        )

    def test_reingesting_same_content_creates_duplicates(
        self, pipeline: IngestionPipeline, vector_db: FakeVectorDB
    ) -> None:
        """Re-ingesting identical content should be skipped, but currently is not."""
        first = pipeline.ingest_readme(profile_id="prof-1", repo_name="my-repo", content=README)
        second = pipeline.ingest_readme(profile_id="prof-1", repo_name="my-repo", content=README)

        # Same content -> same deterministic source_id both times.
        assert first.source_id == second.source_id

        # BUG: the second ingest is NOT skipped (should be True after the fix).
        assert first.skipped is False
        assert second.skipped is False

        # BUG: identical vector ids were written twice -> duplicates in the store.
        assert vector_db.add_calls == 2 * first.chunk_count
        unique_ids = set(vector_db.added_ids)
        assert len(vector_db.added_ids) == 2 * len(unique_ids)
