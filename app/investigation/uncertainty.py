from app.schemas.models import RetrievedEvidence


def detect_uncertainty(
    evidence: list[RetrievedEvidence],
    confidence: float,
) -> list[str]:

    uncertainty = []

    if not evidence:
        uncertainty.append("No relevant historical evidence was retrieved.")

    if confidence < 0.70:
        uncertainty.append(
            "The issue classification has relatively low confidence."
        )

    if evidence and evidence[0].score < 0.30:
        uncertainty.append(
            "The strongest retrieved case has weak similarity to the ticket."
        )

    if len(evidence) == 1:
        uncertainty.append(
            "Only one relevant historical case was found."
        )

    return uncertainty