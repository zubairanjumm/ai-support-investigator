import re

import numpy as np

from app.schemas.models import HistoricalCase, RetrievedEvidence


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"\b\w+\b", text.lower()))


def keyword_score(query: str, document: str) -> float:
    query_tokens = tokenize(query)
    document_tokens = tokenize(document)

    if not query_tokens:
        return 0.0

    return len(query_tokens & document_tokens) / len(query_tokens)


def semantic_score(query_embedding, document_embeddings):
    return np.dot(document_embeddings, query_embedding)


class HybridRetriever:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self.cases: list[HistoricalCase] = []
        self.embeddings = None

    def index(self, cases: list[HistoricalCase]):
        self.cases = cases

        texts = [
            f"{case.title} {case.description} {case.root_cause} "
            f"{case.resolution} {' '.join(case.tags)}"
            for case in cases
        ]

        self.embeddings = self.embedding_model.encode(texts)

    def search(
        self,
        query: str,
        category: str | None = None,
        top_k: int = 5,
    ) -> list[RetrievedEvidence]:

        if not self.cases:
            return []

        query_embedding = self.embedding_model.encode([query])[0]
        semantic_scores = semantic_score(query_embedding, self.embeddings)

        results = []

        for index, case in enumerate(self.cases):
            document = (
                f"{case.title} {case.description} "
                f"{case.root_cause} {case.resolution} "
                f"{' '.join(case.tags)}"
            )

            keyword = keyword_score(query, document)

            category_bonus = 0.15 if category == case.category else 0.0

            score = (
                0.65 * float(semantic_scores[index])
                + 0.20 * keyword
                + category_bonus
            )

            results.append(
                RetrievedEvidence(
                    source_id=case.case_id,
                    source_type="historical_case",
                    title=case.title,
                    content=(
                        f"Problem: {case.description}\n"
                        f"Root cause: {case.root_cause}\n"
                        f"Resolution: {case.resolution}"
                    ),
                    score=score,
                )
            )

        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )[:top_k]