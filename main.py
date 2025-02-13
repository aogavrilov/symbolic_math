from fastapi import FastAPI
from pydantic import BaseModel
from queue import Queue
import threading
import uuid

import lean.run_task as run_lean_task

app = FastAPI()
request_queue = Queue()
results = {}
requested_ids = set()


class TextInput(BaseModel):
    text: str


def process_queue():
    while True:
        request_id, input_data = request_queue.get()
        processed_text = input_data.text.upper()
        result = run_lean_task(str(input_data.text))
        results[request_id] = {"status": "processed", "query": input_data.text, "result": result}
        request_queue.task_done()


threading.Thread(target=process_queue, daemon=True).start()


@app.post("/process")
async def enqueue_request(input_data: TextInput):
    request_id = str(uuid.uuid4())
    request_queue.put((request_id, input_data))
    requested_ids.add(request_id)
    return {"status": "queued", "request_id": request_id}


@app.get("/result/{request_id}")
async def get_result(request_id: str):
    if request_id in results:
        requested_ids.remove(request_id)
        return results.pop(request_id)
    elif request_id in requested_ids:
        return {"status": "processing"}
    else:
        return {"status": "task_not_found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
