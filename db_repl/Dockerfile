# db_slave/Dockerfile
FROM postgres:14

# Копирование скрипта конфигурации
COPY init.sh /docker-entrypoint-initdb.d/

# Даем скрипту права на выполнение
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

