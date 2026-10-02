import json
from pathlib import Path

from app.schemas.models import HistoricalCase, SupportTicket


def load_tickets(path: str | Path) -> list[SupportTicket]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [SupportTicket(**ticket) for ticket in data]


def load_historical_cases(path: str | Path) -> list[HistoricalCase]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [HistoricalCase(**case) for case in data]