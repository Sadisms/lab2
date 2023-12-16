import peewee

from .base_model import BaseModel


class CountriesModel(BaseModel):
    code = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=255)
    capital_city = peewee.CharField(max_length=255)
    population_size = peewee.IntegerField()

    class Meta:
        db_table = 'countries'
