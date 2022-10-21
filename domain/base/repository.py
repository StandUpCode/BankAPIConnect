from typing import TypeVar, Generic
from abc import abstractmethod

from asyncio import sleep
from functools import wraps

from .str_id import StrIdValueObject
from .entity import Entity

IdType = TypeVar('IdType', bound=StrIdValueObject)
EntityType = TypeVar('EntityType', bound=Entity)


class EntityNotFound(Exception):
    pass


class EntityOutdated(Exception):
    pass


class RepositoryAbstract(Generic[IdType, EntityType]):
    @abstractmethod
    async def next_identity(self) -> IdType:
        pass

    @abstractmethod
    async def from_id(self, id_: IdType) -> EntityType:
        pass

    @abstractmethod
    async def save(self, entity: EntityType):
        pass


def transaction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except EntityOutdated:
                await sleep(0.1)

    return wrapper
