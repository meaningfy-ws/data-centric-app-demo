from typing import Optional

from pydantic import BaseModel, Field, AliasChoices
from pydantic_extra_types.phone_numbers import PhoneNumber

from data_centric_app_demo import STRICT_MODEL_CONFIG

class Person(BaseModel):
    model_config = STRICT_MODEL_CONFIG

    id: str = Field(serialization_alias="@id", validation_alias=AliasChoices("id" ,"@id"))
    type: str = Field(serialization_alias="@type", validation_alias=AliasChoices("type", "@type"), default="Person")
    name: str = Field()
    age: int = Field()
    phone: Optional[PhoneNumber] = None