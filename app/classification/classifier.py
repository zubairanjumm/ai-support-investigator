from app.schemas.models import SupportTicket


CATEGORIES = [
    "service_unavailable",
    "performance",
    "authentication",
    "webhook",
    "database",
    "unknown",
]


def classify_ticket(ticket: SupportTicket) -> tuple[str, float]:
    text = f"{ticket.title} {ticket.description}".lower()

    if "503" in text or "service unavailable" in text:
        return "service_unavailable", 0.95

    if "slow" in text or "slowly" in text or "performance" in text:
        return "performance", 0.90

    if "password" in text or "login" in text or "authentication" in text:
        return "authentication", 0.92

    if "webhook" in text:
        return "webhook", 0.95

    if "database" in text or "connection" in text:
        return "database", 0.88

    return "unknown", 0.40