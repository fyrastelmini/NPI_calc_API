from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from utilities import calculate_rpn, insert_into_db

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def calculate(request: Request, text: str = Form(...)):
    try:
        result = calculate_rpn(text)
        insert_into_db(text, result)
    except ValueError as e:
        result = "Erreur: " + str(e)
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": result, "operation": text}
    )
