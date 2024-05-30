import abc


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def transaction(self, data):
        raise NotImplementedError


    @abc.abstractmethod
    def delete(self, data):
        raise NotImplementedError


    @abc.abstractmethod
    def update(self, data):
        raise NotImplementedError