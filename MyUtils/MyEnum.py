from enum import Enum, auto
from typing import Any


class MyEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

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


if __name__ == "__main__":
    class TestEnum(MyEnum):
        test = auto()
        enumz = auto()

    print(
        TestEnum.list(),
        TestEnum('TeSt'),
    )
