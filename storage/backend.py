from abc import ABC, abstractmethod
from typing import Any, List

class StorageBackend(ABC):

    @abstractmethod
    def get(key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> bool:
        pass

    @abstractmethod
    def keys(self, key_pattern: str) -> List[str]:
        pass