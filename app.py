from fastapi import FastAPI
import form_io
from agents import stream_agent
from fastapi.responses import StreamingResponse
from pydantic import BaseModel


class ChatRequest(BaseModel):
    version: int
    message: str
    form_id: str | None

app = FastAPI()


@app.get('/get_all_form_details')
def get_all_form_details():
    return form_io.get_created_forms()


@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {"role": "user", "content": request.message}
    ]

    return StreamingResponse(
        stream_agent(messages),
        media_type="application/json"
    )