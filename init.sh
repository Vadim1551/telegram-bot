#!/bin/bash
set -e

psql -U postgres -d postgres << EOF

DROP ROLE IF EXISTS ${REPL_DB_USER};
DROP ROLE IF EXISTS ${DB_USER};

CREATE ROLE ${REPL_DB_USER} WITH REPLICATION PASSWORD '${REPL_DB_PASSWORD}' LOGIN;
CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}' ENCRYPTED;

DROP DATABASE IF EXISTS ${DB_NAME} CASCADE;
CREATE DATABASE ${DB_NAME};

GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${DB_USER};

\c ${DB_NAME};

CREATE TABLE emails (
  ID SERIAL PRIMARY KEY,
  email VARCHAR(150) NOT NULL
);

CREATE TABLE phones (
  ID SERIAL PRIMARY KEY,
  phone VARCHAR(150) NOT NULL
);

INSERT INTO emails (email) VALUES ('asd@mail.ru'), ('123@yandex.ru');
INSERT INTO phones (phone) VALUES ('+79999991122'), ('89851111111');
EOF
