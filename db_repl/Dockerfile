# db_slave/Dockerfile
FROM postgres:14

# Копирование скрипта конфигурации
COPY setup-replication.sh /docker-entrypoint-initdb.d/

# Даем скрипту права на выполнение
RUN chmod +x /docker-entrypoint-initdb.d/setup-replication.sh

