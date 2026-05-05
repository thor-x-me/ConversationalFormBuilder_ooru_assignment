from fastapi import FastAPI, File, Form, UploadFile
import traceback
from agents import agent
from fastapi.responses import StreamingResponse
import base64
from langchain_core.messages import HumanMessage
import json
from form_io import get_form_data, get_versioned_form, update_form, add_versioned_form, update_versioned_form, get_versioned_form_data

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/get_all_form_details')
def get_all_form_details():
    # return form_io.get_created_forms()
    return {"data": get_versioned_form_data()}

@app.post("/chat")
async def chat(
    version: int | None = Form(default=None),
    form_id: str | None = Form(default=None),
    message: str = Form(...),
    images: list[UploadFile] = File(default=[])
):
    if version is not None:
        #loading the version of form requested by user
        old_form = get_versioned_form(form_id, version)
        update_form(form_id, old_form)
        message = f"This request is for form if: {form_id}\n" + message

    content_list = [{"type": "text", "text": message}]
    
    for img in images:
        image_bytes = await img.read()
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        # Format as a data URL for the image_url block
        content_list.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
        })
    
    # Send as a list of LangChain messages
    messages = [HumanMessage(content=content_list)]
    return StreamingResponse(
        _generate(messages, version, form_id),
        media_type="text/event-stream"
    )

async def _generate(messages, version, form_id):
    async for chunk in agent.astream_events(
        {"messages": messages},
        stream_mode=["messages", "custom"],
        version="v2",
    ):
        event_type = chunk["event"]
        if event_type == "on_chat_model_stream":
            token = chunk["data"]["chunk"].content
            if token:
                yield f"data: {json.dumps({'type': 'llm', 'content': token})}\n\n"

        elif event_type == "on_tool_start":
            tool_name = chunk["name"]
            inputs = chunk["data"].get("input")   # args the LLM passed
            yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_name, 'input': inputs})}\n\n"
        
        elif event_type == "on_tool_end":
            output = chunk["data"].get("output")  
            tool_name = chunk["name"]
            try:
                new_form = json.loads(output.content)
                if tool_name == "create_form":
                    new_form_body = add_versioned_form(new_form.get("_id"), 1, new_form)
                elif tool_name == "update_form":
                    new_form_body = update_versioned_form(form_id, version+1, new_form)

                yield f"data: {json.dumps({'type': 'tool_result', 'tool': tool_name, 'output': new_form_body})}\n\n"
            except:
                pass
