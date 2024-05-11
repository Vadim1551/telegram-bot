import logging
import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv


class DB:
    def __init__(self):
        self.__connection = None
        load_dotenv()
        self.__USERNAME = os.getenv("DB_USER")
        self.__HOST = os.getenv('DB_HOST')
        self.__PORT = os.getenv('DB_PORT')
        self.__DB_NAME = os.getenv('DB_NAME')
        self.__PASSWORD = os.getenv('DB_PASSWORD')

    def executeCommand(self, command):
        try:
            self.__connection = psycopg2.connect(user=self.__USERNAME,
                                          password=self.__PASSWORD,
                                          host=self.__HOST,
                                          port=self.__PORT,
                                          database=self.__DB_NAME)

            cursor = self.__connection.cursor()
            cursor.execute(command)
            if command[:6] == "SELECT":
                data = cursor.fetchall()
                text = ''
                for row in data:
                    text += f"{row}\n"
                logging.info(f"Команда \"{command}\" успешно выполнена")
                return text

            elif command[:6] == "INSERT":
                self.__connection.commit()
                logging.info(f"Команда \"{command}\" успешно выполнена")
                return "Данные успешно записаны"
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
            return "Произошла ошибка"
        finally:
            if self.__connection is not None:
                cursor.close()
                self.__connection.close()
                logging.info("Соединение с PostgreSQL закрыто")
