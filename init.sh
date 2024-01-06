#!/bin/bash

MYSQL_HOST="db"
MYSQL_USER="root"
MYSQL_PASSWORD="student"
DATABASE_NAME="BE_188612"
SQL_FILE="/docker-entrypoint-initdb.d/sqldump.sql"
sleep 5
if mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "use $DATABASE_NAME"; then
    mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "DROP DATABASE $DATABASE_NAME";
fi
sleep 5
mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE $DATABASE_NAME";
sleep 5
mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$DATABASE_NAME" < "$SQL_FILE";
exec apache2-foreground
