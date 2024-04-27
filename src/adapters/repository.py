import abc

from src.models.foaf import Person


class PersonAbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, person: Person):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, person_id: str) -> Person:
        raise NotImplementedError
