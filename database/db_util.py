import os
import psycopg
from dotenv import load_dotenv
from argon2 import PasswordHasher
import argon2

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
            cursor.execute("SELECT password FROM public.users WHERE username LIKE %s;", (username,))

            try:
                PasswordHasher().verify(password=password, hash=cursor.fetchone()[0])
                return 'ok'
            except argon2.exceptions.VerifyMismatchError:
                return 'wrong password'

    def add_user(self, usernameIn, passwordIn, category):
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

    def check_user_exists(self, usernameIn):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.users where username like %s;", (usernameIn,))
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
                batchModel = BatchModel.BatchModel((
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
                return batchModel
            return None

    def add_distributor(self, disModel):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.distributor where id like %s;", (disModel.id,))
            if cursor.fetchone():
                return "already exists"
            cursor.execute("INSERT INTO public.distributor (nama, lokasi, id) VALUES (%s, %s, %s);",
                           disModel.getTuple())
            return "ok"

    def add_peternak(self, peternakModel):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.peternakan where id like %s;", (peternakModel.id,))
            if cursor.fetchone():
                return "already exists"
            cursor.execute("INSERT INTO public.peternakan (nama, lokasi, id) VALUES (%s, %s, %s);",
                           peternakModel.getTuple())
            return "ok"

    def input_batch(self, batchModel):
        with psycopg.connect(conninfo=Postgres_URI) as conn:
            cursor = conn.cursor()
            cursor.execute("select * from public.batch_unggas where id like %s;", (batchModel.id,))
            if cursor.fetchone():
                return "already exists"
            cursor.execute("INSERT INTO public.batch_unggas (id, jenis_ternak, peternak, distributor, berat_rt_sample, tgl_mulai, tgl_potong, tgl_kemas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                           batchModel.getTuple())
            return "ok"


DbUtil = DBUtil()
# print(DbUtil.get_batch_by_id("000001"))
# print(DbUtil.add_distributor("PT Abdul", "Jakarta", "JKT01"))
