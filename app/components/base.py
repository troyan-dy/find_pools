import abc

from starlette.datastructures import State


class BaseComponent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def startup(self, state: State) -> State:
        """Initialize the component and publish its resources in ``state``."""

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """Release the resources acquired in :meth:`startup`."""
