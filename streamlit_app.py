import json

import streamlit as st

from app.ingestion.loader import load_historical_cases, load_tickets
from app.investigation.investigator import SupportInvestigator
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.hybrid import HybridRetriever
from app.schemas.models import SupportTicket


st.set_page_config(
    page_title="AI Support Investigator",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource
def load_investigator():
    embedding_model = EmbeddingModel()

    retriever = HybridRetriever(embedding_model)

    cases = load_historical_cases(
        "data/historical_cases.json"
    )

    retriever.index(cases)

    return SupportInvestigator(retriever)


@st.cache_data
def load_sample_tickets():
    return load_tickets("data/tickets.json")


def display_report(ticket, investigation):
    st.divider()

    st.subheader("Investigation Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Classification",
            investigation.category.replace("_", " ").title(),
        )

    with col2:
        st.metric(
            "Confidence",
            f"{investigation.confidence:.0%}",
        )

    with col3:
        evidence_count = len(investigation.evidence)

        st.metric(
            "Evidence Found",
            evidence_count,
        )

    st.subheader("Issue Summary")

    st.write(
        f"**{ticket.title}**"
    )

    st.write(ticket.description)

    st.subheader("Likely Root Cause")

    st.info(investigation.root_cause)

    st.subheader("Recommended Actions")

    for index, action in enumerate(
        investigation.recommended_actions,
        start=1,
    ):
        st.write(f"{index}. {action}")

    st.subheader("Supporting Evidence")

    if investigation.evidence:
        for index, evidence in enumerate(
            investigation.evidence,
            start=1,
        ):
            with st.expander(f"Historical Case {index}"):
                st.write(evidence)

    else:
        st.warning(
            "No relevant historical evidence was found."
        )

    if investigation.uncertainty:
        st.subheader("Uncertainty")

        for item in investigation.uncertainty:
            st.warning(item)

    else:
        st.subheader("Uncertainty")

        st.success(
            "No significant uncertainty was detected."
        )

    report = {
        "ticket_id": ticket.ticket_id,
        "issue_summary": (
            f"{ticket.title}: {ticket.description}"
        ),
        "classification": investigation.category,
        "confidence": investigation.confidence,
        "likely_root_cause": investigation.root_cause,
        "recommended_actions": (
            investigation.recommended_actions
        ),
        "supporting_evidence": investigation.evidence,
        "uncertainty": investigation.uncertainty,
    }

    st.download_button(
        label="Download Investigation Report",
        data=json.dumps(
            report,
            indent=2,
        ),
        file_name=f"{ticket.ticket_id}_investigation.json",
        mime="application/json",
    )


def main():
    st.title("AI Support Investigator")

    st.caption(
        "Investigate support tickets using historical cases, "
        "semantic similarity, keyword matching, and classification."
    )

    investigator = load_investigator()
    sample_tickets = load_sample_tickets()

    st.sidebar.header("Ticket")

    mode = st.sidebar.radio(
        "Input type",
        [
            "Sample ticket",
            "Custom ticket",
        ],
    )

    if mode == "Sample ticket":
        ticket_options = {
            f"{ticket.ticket_id} — {ticket.title}": ticket
            for ticket in sample_tickets
        }

        selected_label = st.sidebar.selectbox(
            "Select a ticket",
            list(ticket_options.keys()),
        )

        ticket = ticket_options[selected_label]

        st.sidebar.write(
            f"**Customer:** {ticket.customer}"
        )

        st.sidebar.write(
            f"**Product:** {ticket.product}"
        )

        st.sidebar.write(
            f"**Priority:** {ticket.priority}"
        )

    else:
        ticket_id = st.sidebar.text_input(
            "Ticket ID",
            value="CUSTOM-001",
        )

        title = st.sidebar.text_input(
            "Title",
            value="",
        )

        description = st.sidebar.text_area(
            "Description",
            value="",
            height=150,
        )

        customer = st.sidebar.text_input(
            "Customer",
            value="Customer",
        )

        product = st.sidebar.text_input(
            "Product",
            value="Platform",
        )

        priority = st.sidebar.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high",
                "critical",
            ],
        )

        ticket = SupportTicket(
            ticket_id=ticket_id,
            title=title,
            description=description,
            customer=customer,
            product=product,
            priority=priority,
        )

    st.subheader("Support Ticket")

    ticket_col1, ticket_col2 = st.columns(2)

    with ticket_col1:
        st.write(f"**Ticket:** {ticket.ticket_id}")
        st.write(f"**Customer:** {ticket.customer}")
        st.write(f"**Product:** {ticket.product}")

    with ticket_col2:
        st.write(f"**Priority:** {ticket.priority}")
        st.write(f"**Title:** {ticket.title}")

    st.write(ticket.description)

    investigate = st.button(
        "Investigate Ticket",
        type="primary",
        use_container_width=True,
    )

    if investigate:
        if not ticket.title.strip():
            st.error("Ticket title is required.")
            return

        if not ticket.description.strip():
            st.error("Ticket description is required.")
            return

        with st.spinner(
            "Investigating ticket and searching historical cases..."
        ):
            investigation = investigator.investigate(ticket)

        display_report(
            ticket,
            investigation,
        )


if __name__ == "__main__":
    main()