import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
Postgres_URI = os.getenv('POSTGRES_URI')


class DBUtil:
    def _init_(self):
        return

    @staticmethod
    def add_user(usernameIn, passwordIn, category):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO public.users (username, password, role) VALUES(%s, %s, %s);",
                           (usernameIn, passwordIn, category))
            conn.commit()

    @staticmethod
    def remove_user(usernameIn):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM public.users WHERE username LIKE %s;", (usernameIn,))
            conn.commit()

    @staticmethod
    def new_password_user(usernameIn, passwordIn):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE public.users SET password = %s WHERE username LIKE %s;", (passwordIn, usernameIn))
            conn.commit()


DbUtil = DBUtil()
# DbUtil.remove_user('test')
DbUtil.add_user(passwordIn="asd", usernameIn="sad", category="admin")
