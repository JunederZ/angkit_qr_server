import os
import psycopg
from dotenv import load_dotenv
from argon2 import PasswordHasher
import argon2
import json
from models import BatchModel
from models import DistributorModel
from models import PeternakModel

load_dotenv()
Postgres_URI = os.getenv('POSTGRES_URI')


class DBUtil:

    def _init_(self):
        return

    def user_login(self, username, password):
        if not self.check_user_exists(username):
            return "User not exists"
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select password from public.users where username like %s;", (username,))

            try:
                PasswordHasher().verify(password=password, hash=cursor.fetchone()[0])
                return 'ok'
            except argon2.exceptions.VerifyMismatchError as e:
                return 'wrong password'

    def add_user(self, usernameIn, passwordIn, category, json=None):
        if self.check_user_exists(usernameIn):
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
        if not self.check_user_exists(usernameIn):
            return "User not exists"
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM public.users WHERE username LIKE %s;", (usernameIn,))
            conn.commit()

    def new_password_user(self, usernameIn, passwordIn):
        if not self.check_user_exists(usernameIn):
            return "User not exists"
        ph = PasswordHasher()
        hashed_pass = ph.hash(passwordIn)
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE public.users SET password = %s WHERE username LIKE %s;", (hashed_pass, usernameIn))
            conn.db.commit()

    @staticmethod
    def check_user_exists(usenameIn):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.users where username like %s;", (usenameIn,))
            if cursor.fetchone():
                return True
            return False

    def get_batch_by_id(self, id):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM public.batch_unggas where id like %s;", (id,))
            dataBatch = cursor.fetchone()
            if not dataBatch:
                return "not found"
            cursor.execute("SELECT * FROM public.peternakan where id like %s;", (dataBatch[2],))
            dataPeternak = PeternakModel.PeternakModel(cursor.fetchone())
            cursor.execute("SELECT * FROM public.distributor where id like %s;", (dataBatch[3],))
            dataDistributor = DistributorModel.DistributorModel(cursor.fetchone())

            if dataBatch:
                disMode = BatchModel.BatchModel((
                    dataBatch[0],
                    dataBatch[1],
                    dataPeternak,
                    dataDistributor,
                    dataBatch[4],
                    dataBatch[5],
                    dataBatch[6],
                    dataBatch[7],
                    )
                )
                return disMode
            return None


    # def input_batch(self, id, json):
    #     with psycopg.connect(conninfo=Postgres_URI) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT * FROM public.batch_unggas where id like %s;", (id,))
    #         if cursor.fetchone():
    #             return True
    #         return False

DbUtil = DBUtil()
# print(DbUtil.user_login(password="asd", username="sad"))
print(DbUtil.get_batch_by_id("000001"))
