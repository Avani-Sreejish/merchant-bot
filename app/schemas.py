from pydantic import BaseModel
from typing import List

class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: dict

class TickResponse(BaseModel):
    actions: List[dict]

class ReplyRequest(BaseModel):
    conversation_id: str
    reply_text: str
