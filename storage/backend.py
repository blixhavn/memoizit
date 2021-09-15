from abc import ABC, abstractmethod
from typing import Any, List


class StorageBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str) -> int:
        pass

    @abstractmethod
    def keys_startswith(self, key_start: str) -> List[str]:
        pass
