import logging
from typing import Iterator, List

import requests

from data_centric_app_demo.adapters.repository_abc import AbstractRepository
from data_centric_app_demo.models.person import Person


class FlureeDBPersonRepositoryException(Exception):
    pass


class FlureeDBPersonRepository(AbstractRepository):

    def __init__(self,
                 fluree_host: str,
                 fluree_port: int,
                 ledger_name: str) -> None:

        self.fluree_host = fluree_host
        self.fluree_port = fluree_port
        self.ledger_name = ledger_name
        self.fluree_url = f"{self.fluree_host}:{self.fluree_port}"
        self._create_ledger()

    def _create_ledger(self):
        jsonld_request = {
            "@context": "https://w3id.org/webledger/v1",
            "ledger": self.ledger_name,
            "insert": [{
                "@id": "ex:note1",
                "@type": "ex:Note",
                "ex:description": "To create a ledger, you need to provide some initial data, just like you would make an 'initial commit' when using git"
            }]
        }
        response = requests.post(f"{self.fluree_url}/fluree/create", json=jsonld_request)
        if response.status_code == 409:
            logging.info(f"Ledger {self.ledger_name} already exists")
            return
        if response.status_code != 201:
            raise FlureeDBPersonRepositoryException(
                f"Error creating ledger: {response.text}"
            )
        logging.info(f"Created ledger {self.ledger_name}")

    def add(self, person: Person):
        jsonld_request = {
            "ledger": self.ledger_name,
            "insert": [person.model_dump(by_alias=True, exclude_none=True)],
        }
        response = requests.post(f"{self.fluree_url}/fluree/transact", json=jsonld_request)
        if response.status_code != 200:
            raise FlureeDBPersonRepositoryException(
                f"Error adding person: {response.text}"
            )
        logging.info(f"Added person {person.id}")

    def get_by_id(self, person_id: str) -> Person | None:
        jsonld_request = {
            "from": self.ledger_name,
            "where": {
                "@id": person_id,
                "@type": "Person",
            },
            "select": {person_id: ["*"]}
        }
        response = requests.post(f"{self.fluree_url}/fluree/query", json=jsonld_request)
        if response.status_code != 200:
            raise FlureeDBPersonRepositoryException(
                f"Error getting person: {response.text}"
            )
        if not response.json():
            logging.info(f"Person {person_id} not found")
            return None
        return Person.parse_obj(response.json()[0])

    def _get_list_of_persons_id(self) -> List[str]:
        jsonld_request = {
            "from": self.ledger_name,
            "where": {
                "@id": "?s",
                "@type": "Person"
            },
            "select": { "?s": ["@id"] }
        }
        response = requests.post(f"{self.fluree_url}/fluree/query", json=jsonld_request)
        if response.status_code != 200:
            raise FlureeDBPersonRepositoryException(
                f"Error getting list of persons: {response.text}"
            )
        return [person_id["@id"] for person_id in response.json()]

    def list(self) -> Iterator[Person]:
        for person_id in self._get_list_of_persons_id():
            yield self.get_by_id(person_id)

    def delete(self, person_id: str):
        if not self.get_by_id(person_id):
            return

        jsonld_request = {
            "ledger": self.ledger_name,
            "where": {
                "@id": person_id,
                "?p": "?o"
            },
            "delete": {
                "@id": person_id,
                "?p": "?o"
            }
        }
        response = requests.post(f"{self.fluree_url}/fluree/transact", json=jsonld_request)
        if response.status_code != 200:
            raise FlureeDBPersonRepositoryException(
                f"Error deleting person: {response.text}"
            )
        logging.info(f"Deleted person {person_id}")

    def update(self, person: Person):
        raise NotImplementedError
