#!/bin/bash
# Read query into a variable



# If psql is not available, then exit
if ! command -v psql > /dev/null; then
  echo "This script requires psql to be installed and on your PATH ..."
  exit 1
fi

# change dir
cd db

# conn info
source .env

# schema
sql="$(<"schema.sql")"

#connect go drop
CONFIG="dbname=postgres host=$POSTGRES_HOST port=$POSTGRES_PORT user=$POSTGRES_USERNAME password=$POSTGRES_PASSWORD"
psql "$CONFIG" -c "DROP DATABASE IF EXISTS $POSTGRES_DATABASE"
psql "$CONFIG" -c "CREATE DATABASE $POSTGRES_DATABASE"

# Connect to the database, run the query, then disconnect
PGPASSWORD="${POSTGRES_PASSWORD}" psql -t -A \
-h "${POSTGRES_HOST}" \
-p "${POSTGRES_PORT}" \
-d "${POSTGRES_DATABASE}" \
-U "${POSTGRES_USERNAME}" \
-c "${sql}"

# run the install.py script
echo "seeding db"
cd ..
pipenv run python db/install.py