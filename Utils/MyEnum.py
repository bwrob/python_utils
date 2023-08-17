from enum import Enum
from typing import Any


class MyEnum(Enum):

    @classmethod
    def list(cls) -> list[str]:
        return list(map(lambda x: x.name, cls))

    @classmethod
    def _missing_(cls, value: str) -> Any:
        value = value.lower()
        for member in cls:
            if member.name.lower() == value:
                return member
        return None
