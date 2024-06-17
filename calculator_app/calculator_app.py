from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from utilities import calculate_rpn, insert_into_db, view_database

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    """
    Route pour la page d'accueil de l'application.
    Renvoie le template HTML pour la page d'accueil.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def calculate(request: Request, text: str = Form(...)):
    """
    Route pour calculer une expression NPI (Notation Polonaise Inverse).
    Insère le résultat dans la base de données.
    En cas d'erreur de calcul, renvoie un message d'erreur.
    """
    try:
        result = calculate_rpn(text)
        insert_into_db(text, result)
    except ValueError as e:
        result = "Erreur: " + str(e)
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": result, "operation": text}
    )


@app.get("/view_data")
def view_data(request: Request):
    """
    Route pour visualiser les données de la base de données.
    Renvoie le template HTML pour la page de visualisation des données.
    """
    data = view_database()
    return templates.TemplateResponse(
        "view_data.html", {"request": request, "data": data}
    )


@app.get("/download_csv")
def download_csv():
    """
    Route pour télécharger les données de la base de données au format CSV.
    Renvoie un fichier CSV en pièce jointe.
    """
    data = view_database()
    csv = "opération,résultat,date\n"
    for row in data:
        print(row)
        csv += f"{row['operation']},{row['result']},{row['datetime']}\n"
    return Response(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )
