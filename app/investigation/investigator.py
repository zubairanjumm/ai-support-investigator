from app.classification.classifier import classify_ticket
from app.investigation.root_cause import (
    infer_root_cause,
    recommend_actions,
)
from app.investigation.uncertainty import detect_uncertainty
from app.retrieval.reranker import rerank
from app.schemas.models import (
    InvestigationResult,
    SupportTicket,
)


class SupportInvestigator:
    def __init__(self, retriever):
        self.retriever = retriever

    def investigate(self, ticket: SupportTicket) -> InvestigationResult:
        category, confidence = classify_ticket(ticket)

        query = (
            f"{ticket.title} "
            f"{ticket.description} "
            f"{ticket.product}"
        )

        evidence = self.retriever.search(
            query=query,
            category=category,
            top_k=5,
        )

        evidence = rerank(evidence, category)

        root_cause = infer_root_cause(evidence)
        actions = recommend_actions(evidence)
        uncertainty = detect_uncertainty(
            evidence,
            confidence,
        )

        return InvestigationResult(
            ticket_id=ticket.ticket_id,
            category=category,
            confidence=confidence,
            root_cause=root_cause,
            recommended_actions=actions,
            evidence=[
                item.content
                for item in evidence[:3]
            ],
            uncertainty=uncertainty,
        )