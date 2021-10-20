from dataclasses import dataclass


@dataclass
class NumberNode:
    value: float

    def __repr__(self):
        return str(self.value)


@dataclass
class StringNode:
    value: str

    def __repr__(self):
        return f'"{self.value}"'


@dataclass
class AddNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}+{self.node_b})"


@dataclass
class SubtractNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}-{self.node_b})"


@dataclass
class MultiplyNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}*{self.node_b})"


@dataclass
class DivideNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}/{self.node_b})"


@dataclass
class ModuloNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}%{self.node_b})"


@dataclass
class PowerNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}**{self.node_b})"


@dataclass
class PlusNode:
    node: any

    def __repr__(self):
        return f"(+{self.node})"


@dataclass
class MinusNode:
    node: any

    def __repr__(self):
        return f"(-{self.node})"


@dataclass
class BWLeftShiftNode:  # Bitwise Left shift node
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} << {self.node_b})"


@dataclass
class BWRightShiftNode:  # Bitwise Right shift node
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} >> {self.node_b})"


@dataclass
class BWOrNode:  # Bitwise OR node
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} | {self.node_b})"


@dataclass
class BWAndNode:  # Bitwise AND node
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} & {self.node_b})"


@dataclass
class BWXorNode:  # Bitwise XOR node
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a} ^ {self.node_b})"


@dataclass
class BWNotNode:  # Bitwise NOT node
    node: any

    def __repr__(self):
        return f"(~{self.node})"
