from dataclasses import dataclass


@dataclass
class Number:
    value: float

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)


@dataclass
class String:
    value: str

    def __repr__(self):
        return f'"{self.value}"'
