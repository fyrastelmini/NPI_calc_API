#!/bin/bash

# Wait for the database to be ready
until PGPASSWORD=calculator psql -h "calculator_db" -U "calculator" -d "calculator" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"