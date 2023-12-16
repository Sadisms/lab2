from .models.base_model import connection
from .models.countries_model import CountriesModel


def init_tables():
    connection.create_tables([CountriesModel])


def get_countries() -> list:
    select_query = CountriesModel.select()
    if select_query.count() > 0:
        return list(select_query.dicts())

    return list()


def create_country(code: int, name: str, capital_city: str, population_size: int) -> CountriesModel:
    return CountriesModel.create(
        code=code,
        name=name,
        capital_city=capital_city,
        population_size=population_size
    )


def delete_country(code: int, **kwargs) -> int:
    return CountriesModel.delete().where(
        CountriesModel.code == code
    ).execute()


def edit_country(code: int, **kwargs):
    CountriesModel.update(**kwargs).where(
        CountriesModel.code == code
    ).execute()


def get_countries_header_table() -> list[str]:
    return [
        field
        for field in CountriesModel._meta.columns
    ]
