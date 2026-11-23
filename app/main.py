import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)
app = FastAPI(title="Mock Message Service", version="1.0.0")


class MessageRequest(BaseModel):
    token: str
    body: str
    mira_id: str | int
    type: str


def configured_token() -> str:
    token = os.getenv("MESSAGE_SERVICE_TOKEN")
    if not token:
        raise RuntimeError("MESSAGE_SERVICE_TOKEN is required")
    return token


def store_message(message: dict[str, Any]) -> None:
    output_file = os.getenv("MESSAGE_OUTPUT_FILE")
    serialized = json.dumps(message, ensure_ascii=False)
    if not output_file:
        print(serialized, flush=True)
        return
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(serialized + "\n")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/")
def send_message(request: MessageRequest) -> dict[str, str]:
    if request.token != configured_token():
        raise HTTPException(status_code=401, detail="Invalid token")
    store_message(request.model_dump())
    logger.info("Accepted message for mira_id=%s", request.mira_id)
    return {"status": "ok"}
