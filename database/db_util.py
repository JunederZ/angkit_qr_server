import os
import psycopg
from dotenv import load_dotenv
from argon2 import PasswordHasher
import argon2

load_dotenv()
Postgres_URI = os.getenv('POSTGRES_URI')


class DBUtil:

    def _init_(self):
        return

    def user_login(self, username, password):
        if not self.check_user_exist(username):
            return "User not exists"
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select password from public.users where username like %s;", (username,))

            try:
                PasswordHasher().verify(password=password, hash=cursor.fetchone()[0])
                return 'ok'
            except argon2.exceptions.VerifyMismatchError as e:
                return 'wrong password'

    def add_user(self, usernameIn, passwordIn, category):
        if self.check_user_exist(usernameIn):
            return "User already exists"
        ph = PasswordHasher()
        hashed_pass = ph.hash(passwordIn)
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO public.users (username, password, role) VALUES(%s, %s, %s);",
                       (usernameIn, hashed_pass, category))
            conn.commit()
        return "success"

    def remove_user(self, usernameIn):
        if not self.check_user_exist(usernameIn):
            return "User not exists"
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM public.users WHERE username LIKE %s;", (usernameIn,))
            conn.commit()

    def new_password_user(self, usernameIn, passwordIn):
        if not self.check_user_exist(usernameIn):
            return "User not exists"
        ph = PasswordHasher()
        hashed_pass = ph.hash(passwordIn)
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE public.users SET password = %s WHERE username LIKE %s;", (hashed_pass, usernameIn))
            conn.db.commit()

    def check_user_exist(self, usenameIn):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.users where username like %s;", (usenameIn,))
            if cursor.fetchone():
                return True
            return False

DbUtil = DBUtil()
print(DbUtil.user_login(password="assd", username="sad"))
