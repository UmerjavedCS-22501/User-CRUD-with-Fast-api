from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()
File_name = "user_Crud.json"

# load our json file
def load_data():
    if not os.path.exists(File_name):
        return []

    with open(File_name, "r") as f:
        content = f.read().strip()
        if content == "":
            return []
        return json.loads(content)


def save_data(tasks):
    with open(File_name, "w") as f:
        json.dump(tasks, f)

# make pydantic model for validation

class user_data(BaseModel):
    title:Annotated[str,Field(...,description="enter the title that is str")]
    description: Annotated[str,Field(...,description="enter the desceiption")]


class user_update(BaseModel):
    title:Optional[str]
    description:Optional[str]

# home route

@app.get("/")
def home():
    return {"message": "User can add, read, update and delete tasks"}

# route to add task

@app.post("/add_task")
def add_task(task: user_data):
    tasks = load_data()                 # list
    tasks.append(task.model_dump())     # add new task
    save_data(tasks)

    return JSONResponse(
        status_code=200,
        content={"message": "Task added successfully"}
    )
# route to get or see task

@ app.get('/Get_Task/{title}')
def see_task(title:str=Path(...,description='enter your title')):
    tasks=load_data()
    for task in tasks:
        if task["title"]==title:
            return task
        
        
    raise HTTPException(status_code=400,detail="task not found")

#route to update tast by title

@app.put('/update_task/{title}')

def update_task(user:user_update):
    data=load_data()
    for task in data:
        if task['title']==user.title:
            task['description']=user.description
            save_data(data)

            return JSONResponse(
                status_code=200,
                content={"message": "Task updated successfully"}
            )
    raise HTTPException(status_code=404,detail="task not found correct your litle")

#route to del task by title

@app.delete('/delete_task/{title}')
def delete(title:str):
    data= load_data()
    for index,task in enumerate(data):
        if task["title"]==title:
            del data[index]
            save_data(data)
            return JSONResponse(status_code=200,content={'message':'task deleted'})
    raise  HTTPException(status_code=400,detail="task not found")
