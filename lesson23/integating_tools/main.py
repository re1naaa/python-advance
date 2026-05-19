from fastapi import FastAPI
from models import Developer, Project

app = FastAPI()

@app.post("/developers/")
def create_developer(developer: Developer):
    return {"message": "Developer created successfully", "developer": developer}

@app.post("/projects/")
def create_project(project: Project):
    return {"message": "Project created successfully", "project": project}

@app.get("/projects/")
def get_projects():

    sample_project = Project(
        title = "Sample Page",
        description= "This is a sample page",
        language=["Python", "Javascript"],
        lead_developer=Developer(name="Dion Kabashi", experiece=5)
    )
    return {"projects": [sample_project]}