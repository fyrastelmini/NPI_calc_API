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


def insert_into_db(operation: str, result: str):
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
        (operation, result, datetime.now()),
    )

    conn.commit()

    cur.close()
    conn.close()
