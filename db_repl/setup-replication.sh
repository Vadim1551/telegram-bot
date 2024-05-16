#!/bin/bash
set -e

CONFIG_FILE="/var/lib/postgresql/data/postgresql.conf"

# Проверяем существует ли файл конфигурации
if [ -f "$CONFIG_FILE" ]; then
    sed -i 's/^listen_addresses.*/listen_addresses = localhost, ${DB_HOST}/' $CONFIG_FILE
fi

# Останавливаем PostgreSQL
pg_ctl -D /var/lib/postgresql/data stop

sleep 5

rm -rf /var/lib/postgresql/data/*
pg_basebackup -R -h ${DB_HOST} -U ${POSTGRES_USER} -D /var/lib/postgresql/data -P

sleep 1

# Запускаем PostgreSQL
pg_ctl -D /var/lib/postgresql/data start
