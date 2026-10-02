from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AI Support Investigator",
    description="Investigates support tickets using historical cases and semantic retrieval.",
    version="0.1.0",
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "AI Support Investigator",
        "status": "running",
    }