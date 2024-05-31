from __future__ import annotations 
from datetime import (
    datetime,
    date
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic.version import VERSION  as PYDANTIC_VERSION 
if int(PYDANTIC_VERSION[0])>=2:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        field_validator
    )
else:
    from pydantic import (
        BaseModel,
        Field,
        validator
    )

metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass


class Person(ConfiguredBaseModel):
    id: str = Field(...)
    name: str = Field(..., description="""name of the person""")
    aliases: Optional[List[str]] = Field(default_factory=list, description="""other names for the person""")
    phone: Optional[str] = Field(None)
    age: Optional[int] = Field(None, ge=0, le=200)

    @field_validator('phone')
    def pattern_phone(cls, v):
        pattern=re.compile(r"^[\d\(\)\-]+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid phone format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid phone format: {v}")
        return v


class Company(ConfiguredBaseModel):
    id: str = Field(...)
    name: str = Field(..., description="""name of the person""")
    aliases: Optional[List[str]] = Field(default_factory=list, description="""other names for the person""")
    phone: Optional[str] = Field(None)
    employs: Optional[List[Person]] = Field(default_factory=list)

    @field_validator('phone')
    def pattern_phone(cls, v):
        pattern=re.compile(r"^[\d\(\)\-]+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid phone format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid phone format: {v}")
        return v


class Container(ConfiguredBaseModel):
    persons: Optional[List[Person]] = Field(default_factory=list)
    companies: Optional[List[Company]] = Field(default_factory=list)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Person.model_rebuild()
Company.model_rebuild()
Container.model_rebuild()
