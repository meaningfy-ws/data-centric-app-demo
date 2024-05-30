from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from data_centric_app_demo import STRICT_MODEL_CONFIG

class Person(BaseModel):
    model_config = STRICT_MODEL_CONFIG

    id: Field(str)
    name: Field(str)
    age: Field(int)
    phone: Field(Optional[PhoneNumber])