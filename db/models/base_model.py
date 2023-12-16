import peewee


connection = peewee.SqliteDatabase(database='simple_db.db')


class BaseModel(peewee.Model):
    class Meta:
        database = connection
