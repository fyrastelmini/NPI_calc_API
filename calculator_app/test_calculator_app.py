from fastapi.testclient import TestClient
from calculator_app import app
from unittest.mock import patch, MagicMock
from utilities import view_database, insert_into_db, calculate_rpn
from psycopg2 import sql
from datetime import datetime
import pytest

client = TestClient(app)

# ----------------------------------- Tester les fonctions de l'API -----------------------------------


def test_view_database():
    # Créer un mock pour la connexion à la base de données
    mock_conn = MagicMock()
    mock_cur = MagicMock()

    # Configurer le mock pour renvoyer des données spécifiques lorsque fetchall() est appelé
    mock_cur.fetchall.return_value = [(1, "2 2 +", 4, "2022-01-01 00:00:00")]
    mock_conn.cursor.return_value = mock_cur

    # Remplacer psycopg2.connect par le mock lors de l'appel à view_database
    with patch("psycopg2.connect", return_value=mock_conn):
        data = view_database()

    # Vérifier que les données renvoyées sont celles attendues
    assert data == [
        {"id": 1, "operation": "2 2 +", "result": 4, "datetime": "2022-01-01 00:00:00"}
    ]


def test_insert_into_db():
    # Créer un mock pour la connexion à la base de données
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_date = datetime.now()
    # Configurer le mock pour renvoyer des données spécifiques lorsque fetchall() est appelé
    mock_conn.cursor.return_value = mock_cur

    # Remplacer psycopg2.connect par le mock lors de l'appel à insert_into_db
    with patch("psycopg2.connect", return_value=mock_conn):
        insert_into_db("2 2 +", 4, mock_date)

    # Vérifier que la méthode execute a été appelée avec les bonnes valeurs pour la création de la table
    mock_cur.execute.assert_any_call(
        sql.SQL(
            "CREATE TABLE IF NOT EXISTS operations ( id SERIAL PRIMARY KEY, operation VARCHAR(255), result FLOAT, datetime TIMESTAMP );"
        )
    )

    # Vérifier que la méthode execute a été appelée avec les bonnes valeurs pour l'insertion
    mock_cur.execute.assert_any_call(
        sql.SQL(
            "INSERT INTO operations (operation, result, datetime) VALUES (%s, %s, %s)"
        ),
        ("2 2 +", 4, mock_date),
    )

    # Vérifier que execute a été appelée exactement deux fois (création de table + insertion)
    assert len(mock_cur.execute.call_args_list) == 2


def test_calculate_rpn():
    # Tester les cas où l'opération est correcte
    assert calculate_rpn("2 2 +") == 4
    assert calculate_rpn("2 2 *") == 4
    assert calculate_rpn("2 2 /") == 1
    assert calculate_rpn("2 2 -") == 0


# ----------------------------------- Tester les routes -----------------------------------
def test_index_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Calculatrice NPI</title>" in response.text


def test_calculate_route():
    with patch("calculator_app.calculate_rpn") as mock_calculate_rpn, patch(
        "calculator_app.insert_into_db"
    ) as mock_insert_into_db:
        # Définir la valeur de retour de la fonction simulée
        mock_calculate_rpn.return_value = 4

        response = client.post("/", data={"text": "2 2 +"})

        # Vérifier que les fonctions ont été appelées
        mock_calculate_rpn.assert_called_once_with("2 2 +")
        mock_insert_into_db.assert_called_once_with("2 2 +", 4)

        assert response.status_code == 200
        assert "4" in response.text


@pytest.mark.parametrize(
    "input_data,expected_error",
    [
        (
            "22+2",
            "Erreur: Mauvais format d'expression. Utilisez des espaces entre les opérandes et les opérateurs. could not convert string to float: '22+2'",
        ),
        ("22 +", "Erreur: Terme manquant. pop from empty list"),
    ],
)
def test_calculate_route_invalid(input_data, expected_error):
    response = client.post("/", data={"text": input_data})
    assert response.status_code == 400
    assert expected_error in response.text


def test_view_data_route():
    mock_data = [
        {"id": 1, "operation": "2 2 +", "result": 4, "datetime": "2022-01-01 00:00:00"}
    ]

    with patch("calculator_app.view_database", return_value=mock_data):
        response = client.get("/view_data")
        assert response.status_code == 200
        assert "request" in response.context
        assert "data" in response.context
        assert response.context["data"] == mock_data


def test_download_csv_route():
    mock_data = [
        {"id": 1, "operation": "2 2 +", "result": 4, "datetime": "2022-01-01 00:00:00"}
    ]

    with patch("calculator_app.view_database", return_value=mock_data):
        response = client.get("/download_csv")
        assert response.status_code == 200
        assert (
            response.headers["Content-Disposition"] == "attachment; filename=data.csv"
        )
        assert response.content.startswith("opération,résultat,date\n".encode("utf-8"))
