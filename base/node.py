from abc import ABC, abstractmethod

class Node(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._inputs = []
        self._outputs = []

    @abstractmethod
    def spin(self):
        pass

    @abstractmethod
    def _run_onece(self):
        pass
