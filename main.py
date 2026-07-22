import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from pipeline import run_research_pipeline

app = FastAPI()

# Allow frontend to connect (important for JS fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development (later restrict this)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model (kept for the non-streaming route below, if you still want it)
class ResearchRequest(BaseModel):
    topic: str


# Root route (optional)
@app.get("/")
def read_root():
    return {"message": "Multi-Agent Research API is running 🚀"}


def sse_event_generator(topic: str):
    """
    Wraps the pipeline generator and formats each event as
    a Server-Sent-Events (SSE) message: 'data: <json>\\n\\n'
    """
    try:
        for event in run_research_pipeline(topic):
            yield f"data: {json.dumps(event)}\n\n"
    except Exception as e:
        error_event = {"type": "error", "message": str(e)}
        yield f"data: {json.dumps(error_event)}\n\n"


# Streaming route used by the frontend (EventSource requires GET)
@app.get("/research/stream")
def research_stream(topic: str):
    return StreamingResponse(
        sse_event_generator(topic),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # disables proxy buffering (e.g. nginx)
        },
    )


# Kept for backward compatibility / non-streaming clients.
# Runs the whole pipeline and returns only the final result.
@app.post("/research")
def research(request: ResearchRequest):
    final_state = {}
    for event in run_research_pipeline(request.topic):
        if event["type"] == "result":
            final_state = event["data"]
        elif event["type"] == "error":
            return {"error": event["message"]}

    return {
        "search_results": final_state.get("search_results", ""),
        "scraped_content": final_state.get("scraped_content", ""),
        "report": final_state.get("report", ""),
        "feedback": final_state.get("feedback", ""),
    }