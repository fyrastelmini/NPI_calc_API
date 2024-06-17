import psycopg2
from psycopg2 import sql
from datetime import datetime


def calculate_rpn(expression: str) -> float:
    stack = []
    for token in expression.split():
        if token in ["+", "-", "*", "/"]:
            result = 0
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == "+":
                result = operand1 + operand2
            elif token == "-":
                result = operand1 - operand2
            elif token == "*":
                result = operand1 * operand2
            elif token == "/":
                result = operand1 / operand2
            stack.append(result)

        else:
            stack.append(float(token))

    return stack.pop()


def insert_into_db(operation: str, result: str, date=None):
    if date == None:
        date = datetime.now()
    conn = psycopg2.connect(
        dbname="calculator",
        user="calculator",
        password="calculator",
        host="calculator_db",
    )

    cur = conn.cursor()

    cur.execute(
        sql.SQL(
            "CREATE TABLE IF NOT EXISTS operations ( id SERIAL PRIMARY KEY, operation VARCHAR(255), result FLOAT, datetime TIMESTAMP );"
        )
    )

    cur.execute(
        sql.SQL(
            "INSERT INTO operations (operation, result, datetime) VALUES (%s, %s, %s)"
        ),
        (operation, result, date),
    )

    conn.commit()

    cur.close()
    conn.close()


def view_database():
    conn = psycopg2.connect(
        dbname="calculator",
        user="calculator",
        password="calculator",
        host="calculator_db",
    )

    cur = conn.cursor()

    cur.execute(sql.SQL("SELECT * FROM operations;"))

    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(
            {
                "id": row[0],
                "operation": row[1],
                "result": row[2],
                "datetime": str(row[3]),
            }
        )

    cur.close()
    conn.close()

    return data
