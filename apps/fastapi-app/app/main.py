from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Tasks API - FastAPI")

# Armazenamento em memória só pra fase 1.
tasks: list[dict] = []
next_id = 1


class Task(BaseModel):
    title: str
    done: bool = False


@app.get("/health")
def health():
    """Usado pelo healthcheck.py, pelos probes do k8s e pelo Locust."""
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id
    new_task = {"id": next_id, **task.model_dump()}
    tasks.append(new_task)
    next_id += 1
    return new_task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")
