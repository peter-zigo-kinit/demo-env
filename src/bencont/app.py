"""FastAPI app: POST /query → Answer + Tool Calls."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI

import logfire

from bencont.agent import run_query
from bencont.deps import get_deps
from bencont.models import QueryRequest, QueryResponse

load_dotenv()

app = FastAPI(title="Bencont Demo", description="Pydantic AI harness Query API")

# Spec documents LOGFIRE_API_KEY; Logfire's send path keys off a write token.
# Accept either LOGFIRE_TOKEN or LOGFIRE_API_KEY so the documented setup works.
_logfire_token = os.getenv("LOGFIRE_TOKEN") or os.getenv("LOGFIRE_API_KEY")
_send = os.getenv("LOGFIRE_SEND_TO_LOGFIRE", "if-token-present")
if _send.lower() in {"false", "0", "no"}:
    _send_to_logfire: bool | str = False
elif _logfire_token:
    _send_to_logfire = True
else:
    _send_to_logfire = "if-token-present"

logfire.configure(
    send_to_logfire=_send_to_logfire,
    token=_logfire_token,
    service_name="bencont",
    console=False,
)
logfire.instrument_fastapi(app)
logfire.instrument_pydantic_ai()


@app.post("/query", response_model=QueryResponse)
async def post_query(body: QueryRequest) -> QueryResponse:
    answer, tool_calls = await run_query(body.query, deps=get_deps())
    return QueryResponse(answer=answer, tool_calls=tool_calls)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "bencont.app:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
