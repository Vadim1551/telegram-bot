#!/bin/bash

# Путь к файлу pg_hba.conf, поскольку он может отличаться в зависимости от версии PostgreSQL
PG_HBA="/var/lib/postgresql/data/pg_hba.conf"

# Добавление новой строки в конец файла pg_hba.conf
echo "host replication ${REPL_DB_USER} ${REPL_DB_HOST}/32 trust" >> $PG_HBA

CONFIG_FILE="/var/lib/postgresql/data/postgresql.conf"

# Проверяем существует ли файл конфигурации
if [ -f "$CONFIG_FILE" ]; then
    sed -i 's/^#wal_level.*/wal_level = replica/' $CONFIG_FILE
    sed -i 's/^#wal_log_hints.*/wal_log_hints = on/' $CONFIG_FILE
    sed -i 's/^#max_wal_senders.*/max_wal_senders = 10/' $CONFIG_FILE
    sed -i 's/^#archive_mode.*/archive_mode = on/' $CONFIG_FILE
    sed -i "s|^#archive_command.*|archive_command = 'cp %p /oracle/pg_data/archive/%f'|" $CONFIG_FILE
    sed -i 's/^#log_replication_commands.*/log_replication_commands = on/' $CONFIG_FILE
    sed -i "s|^#log_directory.*|log_directory = '/var/lib/postgresql/data/logs'|" $CONFIG_FILE
    sed -i 's/^#logging_collector.*/logging_collector = on/' $CONFIG_FILE
fi

# Останавливаем PostgreSQL
pg_ctl -D /var/lib/postgresql/data stop

# Ждем некоторое время, можно добавить sleep, если это необходимо
sleep 1

# Запускаем PostgreSQL
pg_ctl -D /var/lib/postgresql/data start
