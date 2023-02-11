from pydantic import BaseModel, Field

from utils.fakers.numbers import get_random_number
from utils.fakers.strings import get_random_string


class CreateCustomer(BaseModel):
    customer_name: str = Field(alias='CustomerName')
    contact_name: str = Field(alias='ContactName')
    address: str = Field(alias='Address')
    city: str = Field(alias='City')
    postal_code: str = Field(alias='PostalCode')
    country: str = Field(alias='Country')

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def get_random(cls) -> 'CreateCustomer':
        return CreateCustomer(
            customer_name=get_random_string(),
            contact_name=get_random_string(),
            address=get_random_string(),
            city=get_random_string(),
            postal_code=str(get_random_number()),
            country=get_random_string()
        )

    def columns(self) -> tuple[str, ...]:
        return tuple(self.dict(by_alias=True).keys())

    def values(self) -> tuple[str, ...]:
        return tuple(self.dict().values())

    def join_values(self) -> str:
        values = self.values()
        columns = self.columns()

        return ', '.join([
            f'{column}="{value}"' for column, value in zip(columns, values)
        ])
