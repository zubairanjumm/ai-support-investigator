from app.schemas.models import RetrievedEvidence


def rerank(
    evidence: list[RetrievedEvidence],
    category: str,
) -> list[RetrievedEvidence]:

    for item in evidence:
        if category.lower() in item.content.lower():
            item.score += 0.05

    return sorted(
        evidence,
        key=lambda item: item.score,
        reverse=True,
    )