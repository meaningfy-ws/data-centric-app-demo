import abc


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_id(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, data):
        raise NotImplementedError


    @abc.abstractmethod
    def update(self, data):
        raise NotImplementedError


    @abc.abstractmethod
    def list(self):
        raise NotImplementedError
