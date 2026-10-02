from app.schemas.models import (
    InvestigationResult,
    ResolutionReport,
    SupportTicket,
)


def generate_report(
    ticket: SupportTicket,
    investigation: InvestigationResult,
) -> ResolutionReport:

    return ResolutionReport(
        ticket_id=ticket.ticket_id,
        issue_summary=(
            f"{ticket.title}: {ticket.description}"
        ),
        classification=investigation.category,
        confidence=investigation.confidence,
        likely_root_cause=investigation.root_cause,
        recommended_actions=investigation.recommended_actions,
        supporting_evidence=investigation.evidence,
        uncertainty=investigation.uncertainty,
    )