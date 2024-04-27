from typing import List, Optional

from calamus import fields
from calamus.schema import JsonLDSchema
from pydantic import BaseModel, Field

from src import DEFAULT_MODEL_CONFIG

vocab = "http://xmlns.com/foaf/0.1/"
schema = fields.Namespace(vocab)


class Person(BaseModel):
    model_config = DEFAULT_MODEL_CONFIG

    id: str = Field(serialization_alias='_id')
    first_name: str = Field(serialization_alias='firstName')
    last_name: str = Field(serialization_alias='lastName')
    knows: Optional[List["Person"]] = None
    age: Optional[int] = None


class PersonSchema(JsonLDSchema):
    id = fields.Id()
    first_name = fields.String(schema.firstName)
    last_name = fields.String(schema.lastName)
    knows = fields.Nested(schema.knows, nested='self', many=True)
    age = fields.Integer(schema.age)

    class Meta:
        rdf_type = schema.Person
        model = Person