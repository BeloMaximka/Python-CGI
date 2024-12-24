from data.db import Db
from data.user import User

class UserDao:
    def __init__(self, db: Db):
        self.__db = db


    def create_tables(self):
        with self.__db.get_connection().cursor() as cursor:
            sql = """ CREATE TABLE users (
            `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(128) NOT NULL,
            `email` VARCHAR(256) NOT NULL,
            UNIQUE (name)
            ) ENGINE=InnoDB, DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            cursor.execute(sql)

            sql = """ CREATE TABLE users_access (
            `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
            `user_id` int NOT NULL,
            `password_hash` VARCHAR(64) NOT NULL
            ) ENGINE=InnoDB, DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            cursor.execute(sql)

    def add_user(self, user: User):
        with self.__db.get_connection() as connection:
            cursor = connection.cursor()
            sql = "INSERT INTO users(`name`, `email`) VALUES (%s, %s)"
            cursor.execute(sql, (user.name, user.email))
            sql = "INSERT INTO users_access(`user_id`, `password_hash`) VALUES (%s, %s)"
            cursor.execute(sql, (cursor.lastrowid, user.password_hash))
            connection.commit()

    def get_all_users(self):
        with self.__db.get_connection() as connection:
            cursor = connection.cursor()
            sql = "SELECT id, name, email FROM users"
            cursor.execute(sql)
            rows = cursor.fetchall()

            users = []
            for row in rows:
                users.append(User(id=row[0], name=row[1], email=row[2]))

            return users