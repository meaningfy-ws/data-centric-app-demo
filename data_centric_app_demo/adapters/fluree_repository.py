from typing import List

from aioflureedb import FlureeClient, FlureeTransactionFailure

from data_centric_app_demo.adapters.repository_abc import AbstractRepository


class FlureeRepository(AbstractRepository):

    def __init__(self, ):
        raise NotImplementedError

    def transaction(self, jsonld_data: List[dict]):
        raise NotImplementedError

    def delete(self, data):
        raise NotImplementedError

    def update(self, data):
        raise NotImplementedError