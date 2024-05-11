# Используем официальный образ PostgreSQL версии 14
FROM postgres:14

COPY update-conf.sh /docker-entrypoint-initdb.d/01-update-conf.sh
COPY init.sql /docker-entrypoint-initdb.d/02-init.sql

# Даем скрипту права на выполнение
RUN chmod +x /docker-entrypoint-initdb.d/01-update-conf.sh

USER root

RUN mkdir -p /oracle/pg_data/archive && chown -R postgres:postgres /oracle

WORKDIR /var/lib/postgresql/data
