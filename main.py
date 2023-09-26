from fastapi import FastAPI
from ai_functions import get_lit_survey,get_abstract,get_title

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/lit")
async def get_lit(query:str):
    survey,citation=get_lit_survey(query)
    return {"survey": survey, "citation":citation}

@app.get("/abstract")
async def get_abs(query:str):
    abstract=get_abstract(query)
    return {"abstract":abstract}

@app.get("/title")
async def get_ttl(query:str):
    title=get_title(query)
    return {"title":title}