CREATE ROLE repl_user WITH REPLICATION PASSWORD '123' LOGIN;

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

SELECT pg_reload_conf();
