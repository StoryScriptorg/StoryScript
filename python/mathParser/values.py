from dataclasses import dataclass


@dataclass
class Number:
    value: float

    def __repr__(self):
        return f"{self.value}"


@dataclass
class String:
    value: str

    def __repr__(self):
        return f'"{self.value}"'
