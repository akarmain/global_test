from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.models import init_db, SessionLocal, Task

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Task).where(Task.solved == False).order_by(Task.id.asc()).limit(1)
        )
        first_unsolved = result.scalar_one_or_none()

        if first_unsolved:
            return templates.TemplateResponse(f"tasks/task_{first_unsolved.id}.html", {"request": request, "task": first_unsolved})
        else:
            return templates.TemplateResponse("tasks/completed.html", {"request": request, "task": first_unsolved})


@app.get("/task_{task_id}.html", response_class=HTMLResponse)
async def get_task(request: Request, task_id: int):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return HTMLResponse("Task not found", status_code=404)
        return templates.TemplateResponse(f"tasks/task_{task_id}.html", {"request": request, "task": task})


@app.post("/check_answer/{task_id}")
async def check_answer(task_id: int, user_answer: str = Form(...)):
    async with SessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            return JSONResponse(content={"status": "error", "message": "Task not found"}, status_code=404)
        if task.solved:
            return {"status": "solved"}
        else:
            if user_answer.strip().lower() == task.correct_answer.strip().lower():
                task.solved = True
                await session.commit()
                return {"status": "correct"}
            else:
                return {"status": "incorrect"}
