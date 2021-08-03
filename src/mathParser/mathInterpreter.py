from .values import Number, String


class Interpreter:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    @staticmethod
    def visit_NumberNode(node):
        return Number(node.value)

    @staticmethod
    def visit_StringNode(node):
        return String(node.value)

    def visit_PlusNode(self, node):
        return self.visit(node.node)

    def visit_MinusNode(self, node):
        return Number(-self.visit(node.node).value)

    def visit_AddNode(self, node):
        node_a_val = self.visit(node.node_a).value
        node_b_val = self.visit(node.node_b).value
        if isinstance(node_a_val, str) and isinstance(node_b_val, str):
            return String(node_a_val + node_b_val)
        return Number(node_a_val + node_b_val)

    def visit_SubtractNode(self, node):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

    def visit_MultiplyNode(self, node):
        node_a_val = self.visit(node.node_a).value
        node_b_val = self.visit(node.node_b).value
        if isinstance(node_a_val, str) and isinstance(node_b_val, float):
            return String(node_a_val * int(node_b_val))
        return Number(node_a_val * node_b_val)

    def visit_DivideNode(self, node):
        return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)

    def visit_PowerNode(self, node):
        return Number(self.visit(node.node_a).value ** self.visit(node.node_b).value)

    def visit_ModuloNode(self, node):
        return Number(self.visit(node.node_a).value % self.visit(node.node_b).value)
