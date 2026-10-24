import abc

from starlette.datastructures import State


class BaseComponent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def startup(self, state: State) -> State:
        pass

    @abc.abstractmethod
    async def shutdown(self) -> None:
        pass
