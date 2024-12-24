import mysql.connector
from data.db_config import db_config

class Db:
    def __init__(self):
        self.__connection = None

    def get_connection(self):
        if self.__connection is None:
            self.__connection = mysql.connector.connect(**db_config)
        return self.__connection