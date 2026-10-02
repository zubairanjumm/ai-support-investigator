from app.schemas.models import RetrievedEvidence


def infer_root_cause(evidence: list[RetrievedEvidence]) -> str:
    if not evidence:
        return "Insufficient evidence to determine a likely root cause."

    return evidence[0].content.split("Root cause: ", 1)[-1].split(
        "\n",
        1,
    )[0]


def recommend_actions(evidence: list[RetrievedEvidence]) -> list[str]:
    if not evidence:
        return [
            "Collect additional diagnostic information.",
            "Review recent system changes and service logs.",
        ]

    resolution = evidence[0].content.split("Resolution: ", 1)[-1]

    return [
        resolution.strip(),
        "Verify the result using application and infrastructure metrics.",
    ]