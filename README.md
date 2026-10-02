# AI Support Investigator

**Live App:** [Open the Streamlit App](https://ai-support-investigator-ztmdusnnhbo7ugcrqeqmmi.streamlit.app/?utm_source=chatgpt.com)

AI Support Investigator is a support-ticket investigation system that uses **semantic search, keyword matching, classification, reranking, and historical support cases** to investigate new customer issues.

It finds similar historical incidents, identifies a likely root cause, recommends actions, and produces a structured investigation report.

---

## What It Does

A support engineer receives a new ticket such as:

> "Our API is suddenly returning 503 Service Unavailable errors."

Instead of manually searching through previous support cases, the system:

1. Classifies the support ticket.
2. Creates a semantic representation of the issue.
3. Searches historical support cases.
4. Combines semantic similarity with keyword matching.
5. Reranks the retrieved evidence.
6. Identifies a likely root cause.
7. Recommends actions based on previous resolutions.
8. Reports uncertainty when evidence is weak or incomplete.

---

## How It Works

```text
                    Support Ticket
                          │
                          ▼
                   Ticket Classification
                          │
                          ▼
                    Search Query
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Semantic Search          Keyword Search
              │                       │
              └───────────┬───────────┘
                          ▼
                   Hybrid Retrieval
                          │
                          ▼
                       Reranking
                          │
                          ▼
                  Historical Evidence
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
         Root Cause              Actions
              │                       │
              └───────────┬───────────┘
                          ▼
                  Investigation Report
```

---

## Example

### Input

```text
Title:
API requests suddenly returning 503

Description:
Our application was working normally this morning,
but API requests are now returning 503 Service
Unavailable errors.
```

### Investigation

The system classifies the issue as:

```text
Service Unavailable
Confidence: 95%
```

It then finds similar historical cases.

One relevant historical case identifies:

```text
Root Cause:
The payment service exceeded its connection pool
capacity during a traffic spike.
```

The system uses that historical evidence to produce recommended actions and supporting evidence.

---

## AI Techniques Used

### Semantic Embeddings

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

to convert support tickets and historical cases into numerical embeddings.

This allows the system to find cases that are semantically similar even when the wording is different.

### Keyword Matching

The system also compares words between the new ticket and historical cases.

### Hybrid Retrieval

Semantic similarity and keyword matching are combined:

```text
Semantic similarity
        +
Keyword similarity
        +
Category bonus
        ↓
Combined retrieval score
```

### Reranking

Retrieved cases are reranked using the detected ticket category so that more relevant evidence appears first.

### Uncertainty Detection

The system checks whether:

* No evidence was retrieved.
* Classification confidence is low.
* Retrieved evidence has weak similarity.
* Only one relevant case was found.

---

## Current Architecture

```text
Streamlit GUI
      │
      ▼
Support Investigator
      │
      ├── Classification
      │
      ├── Hybrid Retriever
      │      ├── Embeddings
      │      └── Keyword Matching
      │
      ├── Reranking
      │
      ├── Root Cause Inference
      │
      ├── Action Recommendation
      │
      └── Uncertainty Detection
             │
             ▼
       Investigation Report
```

The project also contains a FastAPI API layer for programmatic access.

---

## Project Structure

```text
ai-support-investigator/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── classification/
│   │   └── classifier.py
│   │
│   ├── generation/
│   │   └── report.py
│   │
│   ├── ingestion/
│   │   └── loader.py
│   │
│   ├── investigation/
│   │   ├── investigator.py
│   │   ├── root_cause.py
│   │   └── uncertainty.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── hybrid.py
│   │   └── reranker.py
│   │
│   ├── schemas/
│   │   └── models.py
│   │
│   └── main.py
│
├── data/
│   ├── historical_cases.json
│   └── tickets.json
│
├── streamlit_app.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

---

## Running Locally

Clone the repository and enter the project:

```bash
git clone https://github.com/zubairanjumm/ai-support-investigator.git
cd ai-support-investigator
```

Install dependencies with `uv`:

```bash
uv sync
```

Run the Streamlit application:

```bash
uv run streamlit run streamlit_app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## Using the Application

The interface supports two modes:

### Sample Ticket

Select one of the included historical test tickets and investigate it.

### Custom Ticket

Enter:

* Ticket ID
* Title
* Description
* Customer
* Product
* Priority

Then click:

```text
Investigate Ticket
```

The application returns:

* Classification
* Confidence
* Likely root cause
* Recommended actions
* Supporting evidence
* Uncertainty

Investigation reports can also be downloaded as JSON.

---

## API

The project also exposes a FastAPI endpoint:

```text
POST /api/investigate
```

A support ticket can be sent to the endpoint and the investigation report is returned as structured data.

Run the API locally with:

```bash
uv run uvicorn app.main:app --reload
```

---

## Important Note

The current version **does not use an external LLM or inference API**.

There is no OpenAI, Gemini, or Hugging Face inference API call involved in the current investigation pipeline.

The AI component currently relies on:

* Sentence Transformer embeddings
* Semantic similarity
* Keyword matching
* Classification rules
* Reranking
* Historical-case reasoning
* Uncertainty detection

This keeps the current application independent of paid LLM APIs.

---

## Tech Stack

* **Python**
* **FastAPI**
* **Streamlit**
* **Pydantic**
* **Sentence Transformers**
* **NumPy**
* **uv**
* **JSON**

---

## Purpose

This project demonstrates how a support investigation system can combine **retrieval, semantic similarity, classification, evidence ranking, and historical incident analysis** to help support engineers investigate recurring technical problems more efficiently.
