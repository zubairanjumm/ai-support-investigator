from fastapi import APIRouter

from app.classification.classifier import classify_ticket
from app.generation.report import generate_report
from app.ingestion.loader import load_historical_cases
from app.investigation.investigator import SupportInvestigator
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.hybrid import HybridRetriever
from app.schemas.models import SupportTicket


router = APIRouter()

embedding_model = EmbeddingModel()
retriever = HybridRetriever(embedding_model)

cases = load_historical_cases("data/historical_cases.json")
retriever.index(cases)

investigator = SupportInvestigator(retriever)


@router.post("/investigate")
def investigate_ticket(ticket: SupportTicket):
    result = investigator.investigate(ticket)
    return generate_report(ticket, result)