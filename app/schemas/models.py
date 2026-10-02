from pydantic import BaseModel, Field


class SupportTicket(BaseModel):
    ticket_id: str
    title: str
    description: str
    customer: str
    product: str
    priority: str


class HistoricalCase(BaseModel):
    case_id: str
    title: str
    description: str
    root_cause: str
    resolution: str
    category: str
    tags: list[str] = Field(default_factory=list)


class SupportDocument(BaseModel):
    document_id: str
    title: str
    content: str
    category: str
    tags: list[str] = Field(default_factory=list)


class InvestigationResult(BaseModel):
    ticket_id: str
    category: str
    confidence: float
    root_cause: str
    recommended_actions: list[str]
    evidence: list[str]
    uncertainty: list[str]


class ResolutionReport(BaseModel):
    ticket_id: str
    issue_summary: str
    classification: str
    confidence: float
    likely_root_cause: str
    recommended_actions: list[str]
    supporting_evidence: list[str]
    uncertainty: list[str]