#!/bin/bash

source .env

set -e

PG_HBA="/etc/postgresql/16/main/pg_hba.conf"

# Добавление новой строки в конец файла pg_hba.conf
echo "host replication ${REPL_DB_USER} ${REPL_DB_HOST}/32 md5" >> $PG_HBA
echo "local   all     all     trust" >> $PG_HBA
#echo "host    replication     all     127.0.0.1/32    scram-sha-256" >> $PG_HBA
#echo "host    replication     all     ::1/128 scram-sha-256" >> $PG_HBA
#echo "host    all     all     127.0.0.1/32    scram-sha-256" >> $PG_HBA
#echo "host    all     all     ::1/128 scram-sha-256" >> $PG_HBA
#echo "local all all trust" >> $PG_HBA



psql -U postgres -d postgres <<EOF
    DROP DATABASE IF EXISTS $DB_NAME;
    CREATE DATABASE $DB_NAME;
    DROP ROLE IF EXISTS $REPL_DB_USER;
    DROP ROLE IF EXISTS $DB_USER;
    CREATE ROLE $REPL_DB_USER WITH REPLICATION PASSWORD '$REPL_DB_PASSWORD' LOGIN;
    CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASSWORD';
    \c $DB_NAME;
    CREATE TABLE IF NOT EXISTS emails (
        ID SERIAL PRIMARY KEY,
        email VARCHAR(150) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS phones (
        ID SERIAL PRIMARY KEY,
        phone VARCHAR(150) NOT NULL
    );
    INSERT INTO emails (email) VALUES ('asd@mail.ru'), ('123@yandex.ru');
    INSERT INTO phones (phone) VALUES ('+79999991122'), ('89851111111');
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
    GRANT ALL PRIVILEGES ON emails, phones TO $DB_USER;
    SELECT pg_reload_conf();
EOF
