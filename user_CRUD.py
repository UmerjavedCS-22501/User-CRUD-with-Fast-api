from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from fastapi.responses import JSONResponse
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
File_name = "user_Crud.json"

# load our json file
def load_data():
    try:
        if not os.path.exists(File_name):
            return []

        with open(File_name, "r") as f:
            content = f.read().strip()
            if content == "":
                return []
            return json.loads(content)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return []


# make pydantic model for validation

class user_data(BaseModel):
    title: Annotated[str, Field(..., description="enter the title that is str")]
    description: Annotated[str, Field(..., description="enter the description")]


class user_update(BaseModel):
    title: Optional[str]
    description: Optional[str]

# home route

@app.get("/")
def home():
    return {"message": "User can add, read, update and delete tasks"}

# route to add task

@app.post("/add_task")
def add_task(task: user_data):
    try:
        tasks = load_data()                 # list
        tasks.append(task.dict())     # add new task
        save_data(tasks)

        return JSONResponse(
            status_code=200,
            content={"message": "Task added successfully"}
        )
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# route to get or see task

@app.get('/Get_Task/{title}')
def see_task(title: str = Path(..., description='enter your title')):
    try:
        tasks = load_data()
        for task in tasks:
            if task["title"] == title:
                return task
        raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        logging.error(f"Error getting task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# route to update task by title

@app.put('/update_task/{title}')
def update_task(title: str, user: user_update):
    try:
        data = load_data()
        for task in data:
            if task['title'] == title:
                if user.title:
                    task['title'] = user.title
                if user.description:
                    task['description'] = user.description
                save_data(data)

                return JSONResponse(
                    status_code=200,
                    content={"message": "Task updated successfully"}
                )
        raise HTTPException(status_code=404, detail="task not found correct your title")
    except Exception as e:
        logging.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# route to delete task by title

@app.delete('/delete_task/{title}')
def delete_task(title: str):
    try:
        data = load_data()
        for index, task in enumerate(data):
            if task["title"] == title:
                del data[index]
                save_data(data)
                return JSONResponse(status_code=200, content={'message': 'task deleted'})
        raise HTTPException(status_code=404, detail="task not found")
    except Exception as e:
        logging.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# save data to json file
def save_data(data):
    try:
        with open(File_name, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Error saving data: {e}")