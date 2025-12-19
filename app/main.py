from fastapi import FastAPI, HTTPException

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # Do absolutely nothing if dotenv is not available
    pass

from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.orchestrator import orchestrate

app = FastAPI(title="Spike AI Backend")


@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    if not req.query:
        raise HTTPException(status_code=400, detail="Query is required")

    result = orchestrate(req.query, req.propertyId)

    return QueryResponse(**result)
