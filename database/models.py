from peewee import *
from dotenv import load_dotenv
from playhouse.db_url import connect
import os

load_dotenv()
db = connect(os.getenv("POSTGRES_URI"))


class UnknownField(object):
    def __init__(self, *_, **__): pass


class ISODateField(DateField):
    field_type = 'date'

    def db_value(self, value):
        return value

    def python_value(self, value):
        if value:
            return value.isoformat()
        return None


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    password = CharField()
    role = CharField(null=True)
    username = CharField(primary_key=True)

    class Meta:
        table_name = 'users'


class Distributor(BaseModel):
    id = CharField(primary_key=True)
    lokasi = CharField()
    nama = CharField()
    user = ForeignKeyField(column_name='username', field='username', model=Users, backref='distributors')

    class Meta:
        table_name = 'distributor'


class Peternakan(BaseModel):
    id = CharField(primary_key=True)
    lokasi = CharField()
    nama = CharField()
    user = ForeignKeyField(column_name='username', field='username', model=Users, backref='peternakan')

    class Meta:
        table_name = 'peternakan'


class BatchUnggas(BaseModel):
    berat_rt_sample = DoubleField(null=True)
    distributor = ForeignKeyField(Distributor, column_name='distributor')
    id = CharField(primary_key=True)
    jenis_ternak = CharField()
    peternak = ForeignKeyField(Peternakan, column_name='peternak', backref='batches')
    tgl_kemas = ISODateField(null=True)
    tgl_mulai = ISODateField()
    tgl_potong = ISODateField(null=True)

    class Meta:
        table_name = 'batch_unggas'


class BatchImages(BaseModel):
    id = AutoField(primary_key=True)
    batch_id = ForeignKeyField(BatchUnggas, to_field='id', column_name='batch_id', backref='images')
    filename = CharField()

    class Meta:
        table_name = 'batch_images'


if __name__ == '__main__':
    db.connect()
    db.create_tables([BatchImages])
