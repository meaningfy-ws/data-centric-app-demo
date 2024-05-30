from typing import Iterator

from data_centric_app_demo.adapters.repository_abc import AbstractRepository
from data_centric_app_demo.models.person import Person

class FlureeDBPersonRepositoryException(Exception):
    pass

class FlureeDBPersonRepository(AbstractRepository):

    def __init__(self,
                 fluree_host: str,
                 fluree_port: int):

        self.fluree_host = fluree_host
        self.fluree_port = fluree_port

    def add(self, person: Person):
        print(person.model_dump_json())

    def get_by_id(self, person_id: str) -> Person | None:
        raise NotImplementedError

    def list(self) -> Iterator[Person]:
        raise NotImplementedError

    def delete(self, person_id: str):
        raise NotImplementedError

    def update(self, person: Person):
        raise NotImplementedError
