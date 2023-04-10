from fastapi import APIRouter
from starlette.exceptions import HTTPException

from .models import Todo
from .database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
)

router = APIRouter()

@router.get("/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@router.get("/todo/{id}", response_model=Todo)
async def get_todo_by_id(id):
    response = await fetch_one_todo(id)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the id {id}")

@router.post("/todo/", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@router.put("/todo/{id}/", response_model=Todo)
async def put_todo(id: str, hidden: bool):
    response = await update_todo(id, hidden)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the id {id}")

@router.delete("/todo/{id}")
async def delete_todo(id):
    response = await remove_todo(id)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the id {id}")