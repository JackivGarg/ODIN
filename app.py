from random import choice
from typing import Literal, TypedDict

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field


STATUS_CODES = [200, 201, 400, 429, 500, 503]


class Message(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    recipient: str = Field(min_length=1)
    message: str = Field(min_length=1)


class DeliveryState(TypedDict):
    recipient: str
    message: str
    history: list[int]
    status: str


def try_send(state: DeliveryState) -> dict:
    status_code = choice(STATUS_CODES)
    return {"history": [*state["history"], status_code]}


def route_after_first(state: DeliveryState) -> Literal["finish", "retry"]:
    return "finish" if 200 <= state["history"][-1] < 300 else "retry"


def finish(state: DeliveryState) -> dict:
    status_code = state["history"][-1]
    return {"status": "sent" if 200 <= status_code < 300 else "failed"}


def build_workflow():
    graph = StateGraph(DeliveryState)
    graph.add_node("first_attempt", try_send)
    graph.add_node("retry", try_send)
    graph.add_node("finish", finish)
    graph.add_edge(START, "first_attempt")
    graph.add_conditional_edges("first_attempt", route_after_first)
    graph.add_edge("retry", "finish")
    graph.add_edge("finish", END)
    return graph.compile()


workflow = build_workflow()
app = FastAPI(
    title="Message retry simulation",
    description="Local random status simulation. No real messages or LLM calls.",
)


@app.post("/send")
def send(request: Message):
    result = workflow.invoke({
        "recipient": request.recipient,
        "message": request.message,
        "history": [],
        "status": "pending",
    })
    status_code = result["history"][-1]
    return JSONResponse(status_code=status_code, content={
        "simulation": True,
        "status": result["status"],
        "status_code": status_code,
        "attempts": len(result["history"]),
        "history": result["history"],
    })
