from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from .utils import calculate_rpn

app = FastAPI()

templates = Jinja2Templates(directory="calculator_app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def calculate(request: Request, text: str = Form(...)):
    try:
        result = calculate_rpn(text)
    except Exception as e:
        result = "Erreur: " + str(e)
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "operation": text})