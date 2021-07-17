#!/bin/bash
# Read query into a variable




# If psql is not available, then exit
if ! command -v psql > /dev/null; then
  echo "This script requires psql to be installed and on your PATH ..."
  exit 1
fi

# change dir
cd db

# args
POSTGRES_HOST=$1
POSTGRES_PORT=$2
POSTGRES_USERNAME=$3
POSTGRES_DATABASE="residence_management"

echo -n POSTGRES PASSWORD: 
read -s POSTGRES_PASSWORD
echo

# Run Command
# echo $POSTGRES_PASSWORD

# schema
sql="$(<"schema.sql")"

#connect go drop
CONFIG="dbname=postgres host=$POSTGRES_HOST port=$POSTGRES_PORT user=$POSTGRES_USERNAME password=$POSTGRES_PASSWORD"
psql "$CONFIG" -c "DROP DATABASE IF EXISTS $POSTGRES_DATABASE"
psql "$CONFIG" -c "CREATE DATABASE residence_management"

# Connect to the database, run the query, then disconnect
PGPASSWORD="${POSTGRES_PASSWORD}" psql -t -A \
-h "${POSTGRES_HOST}" \
-p "${POSTGRES_PORT}" \
-d "${POSTGRES_DATABASE}" \
-U "${POSTGRES_USERNAME}" \
-c "${sql}"

# run the install.py script
echo "instantiating db"
cd ..
pipenv install
pipenv run python db/install.py