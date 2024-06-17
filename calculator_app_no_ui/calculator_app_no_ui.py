from fastapi import FastAPI, HTTPException, Response
from utilities import calculate_rpn, insert_into_db, view_database

app = FastAPI()


@app.get("/")
def home():
    """
    Route pour la page d'accueil de l'application.
    Renvoie un message de bienvenue.
    """
    return {
        "message": "Bienvenue sur l'API de calculatrice NPI! Utilisez /calculate pour effectuer un calcul, /view_data pour visualiser les données, ou /download_csv pour télécharger les données au format CSV."
    }


@app.post("/calculate")
async def calculate(text: str):
    """
    Route pour calculer une expression NPI (Notation Polonaise Inverse).
    Insère le résultat dans la base de données.
    En cas d'erreur de calcul, renvoie un message d'erreur.
    - **text**: L'expression NPI à calculer.
    IMPORTANT: Il faut mettre des espaces entre les opérandes et les opérateurs.
    """
    try:
        result = calculate_rpn(text)
        insert_into_db(text, result)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Erreur: Mauvais format d'expression. Utilisez des espaces entre les opérandes et les opérateurs. "
            + str(e),
        ) from e
    except IndexError as e:
        raise HTTPException(
            status_code=400, detail="Erreur: Terme manquant. " + str(e)
        ) from e
    return {"operation": text, "result": result}


@app.get("/view_data")
def view_data():
    """
    Route pour visualiser les données de la base de données.
    Renvoie les données sous forme de JSON.
    """
    data = view_database()
    return {"data": data}


@app.get("/download_csv")
def download_csv():
    """
    Route pour télécharger les données de la base de données au format CSV.
    Renvoie un fichier CSV en pièce jointe.
    """
    data = view_database()
    csv = "opération,résultat,date\n"
    for row in data:
        csv += f"{row['operation']},{row['result']},{row['datetime']}\n"
    return Response(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )
