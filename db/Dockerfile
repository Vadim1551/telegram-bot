# Используем официальный образ PostgreSQL версии 14
FROM postgres:14

COPY init.sh /docker-entrypoint-initdb.d/init.sh

# Даем скрипту права на выполнение
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

USER root

RUN mkdir -p /oracle/pg_data/archive && chown -R postgres:postgres /oracle

WORKDIR /var/lib/postgresql/data

# Определяем переменные окружения
ENV POSTGRES_DB=""
ENV POSTGRES_USER=""
ENV POSTGRES_PASSWORD=""
ENV REPL_DB_USER=""
ENV REPL_DB_PASSWORD=""
ENV REPL_DB_HOST=""
