from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('angkit_hci', user='ktsabit', host='localhost', port=5432)


class User(Model):
    username = CharField(primary_key=True)
    password = CharField()
    role = CharField()

    class Meta:
        database = db


class Farms(Model):
    id = CharField(primary_key=True)
    name = CharField()
    location = CharField()
    user = ForeignKeyField(User, to_field='username')

    class Meta:
        database = db


class Distrbs(Model):
    id = CharField(primary_key=True)
    name = CharField()
    location = CharField()
    user = ForeignKeyField(User, to_field='username')

    class Meta:
        database = db


class Batch(Model):
    id = CharField(primary_key=True)
    type = CharField()
    farm = ForeignKeyField(Farms)
    distributor = ForeignKeyField(Distrbs)
    avg_weight = DoubleField()
    start_date = DateField()
    end_date = DateField()
    packaging_date = DateField()

    class Meta:
        database = db


db.connect()
