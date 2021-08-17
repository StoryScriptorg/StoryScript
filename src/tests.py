""" TESTING CASES """
import unittest
import processor
from os import remove as delete_file
import sys
import numpy as np
import mathParser.values
import mathParser.tokens
import mathParser.nodes
import mathParser.mathParser


class TestReturnedValue(unittest.TestCase):
    def test_arithmatics(self):
        self.assertEqual(processor.execute("// Arithmatics test"), None)
        self.assertEqual(processor.execute("5 + 5 * 0"), 5)
        self.assertEqual(processor.execute("10 + 20 * 2"), 50)
        self.assertEqual(processor.execute("2 ** 2"), 4)  # (Exponentiation)
        self.assertEqual(processor.execute("3 ^ 2"), 1)  # (Bitwise XOR)
        self.assertEqual(processor.execute("2 | 3"), 3)  # (Bitwise OR)
        self.assertEqual(processor.execute("3 & 3"), 3)  # (Bitwise AND)
        self.assertEqual(processor.execute("3 << 3"), 24)  # (Bitwise Left shift)
        self.assertEqual(processor.execute("3 >> 3"), 0)  # (Bitwise Right shift)
        self.assertEqual(processor.execute("~3"), -4)  # (Bitwise NOT)
        self.assertEqual(
            processor.execute("2 / 0"),
            "DivideByZeroException: You cannot divide numbers with 0",
        )
        self.assertEqual(processor.execute('"e" + "h"'), '"eh"')
        self.assertEqual(processor.execute("'e' + 'h'"), '"eh"')
        self.assertEqual(processor.execute('"e" * 3'), '"eee"')
        self.assertEqual(processor.execute('(+7)+(+7)'), 14)
        self.assertEqual(processor.execute('(-7)+(-7)'), -14)
        self.assertEqual(processor.execute('1 > 2'), "InvalidSyntax: Comparison operator is not allowed in math expression yet.")
        self.assertEqual(processor.execute('1 < 2'), "InvalidSyntax: Comparison operator is not allowed in math expression yet.")
        self.assertEqual(processor.execute('"e\\nh"'), '"e\nh"')
        self.assertEqual(processor.execute('"e\\th"'), '"e\th"')
        self.assertEqual(processor.execute('"e\\"h"'), '"e\"h"')
        self.assertEqual(processor.execute('"e\\\'h"'), '"e\'h"')
        self.assertEqual(processor.execute('"e\\\\h"'), '"e\\h"')
        self.assertEqual(processor.execute('.234.'), "InvalidSyntax: Invalid floating point value \".234. \"")
        self.assertEqual(processor.execute(".234"), mathParser.values.Number(0.234))
        self.assertEqual(processor.execute("234."), 234)
        self.assertEqual(processor.execute("234 567"), "InvalidSyntax: None")
        self.assertEqual(mathParser.mathParser.Parser([None]).parse(), None)
        self.assertEqual(processor.execute("(2 + 3"), "InvalidSyntax: Right parenthesis not found.")
        self.assertEqual(processor.execute(")"), "InvalidSyntax: None")

    def test_exceptions(self):
        self.assertEqual(
            processor.execute("throw InvalidValue \"Description\""),
            "InvalidValue: Description",
        )
        self.assertEqual(
            processor.execute('throw InvalidSyntax "You did something wrong!"'),
            "InvalidSyntax: You did something wrong!",
        )
        self.assertEqual(
            processor.execute('throw AlreadyDefined "This person is already defined."'),
            "AlreadyDefined: This person is already defined.",
        )
        self.assertEqual(
            processor.execute(
                "throw NotImplementedException \"This feature is in Alpha. Please add a Alpha tester profile to use this Feature.\""
            ),
            "NotImplementedException: This feature is in Alpha. Please add a Alpha tester profile to use this Feature.",
        )
        self.assertEqual(
            processor.execute("throw GeneralException"),
            "GeneralException: No Description provided",
        )
        self.assertEqual(
            processor.execute("throw DivideByZeroException"),
            "DivideByZeroException: You cannot divide numbers with 0",
        )
        self.assertEqual(
            processor.execute(
                "throw InvalidTypeException \"The input type cannot be an Iterable data.\""
            ),
            "InvalidTypeException: The input type cannot be an Iterable data.",
        )
        self.assertEqual(
            processor.execute("throw NotDefinedException \"The key is not defined!\""),
            "NotDefinedException: The key is not defined!",
        )
        self.assertEqual(
            processor.execute("throw NotDefinedException e"),
            "InvalidSyntax: Unknown character \"e\" in Math expression at character 1 in expression \"e \".",
        )
        self.assertEqual(
            processor.execute("throw h"),
            "InvalidValue: The Exception entered is not defined",
        )

    def test_other(self):
        processor.syntax_highlighting("")
        processor.syntax_highlighting("\"Hello, world!\"")
        processor.syntax_highlighting("int a = 10 + 10")
        self.assertEqual(str(mathParser.values.Number(5)), "5")
        self.assertEqual(str(mathParser.tokens.Token(mathParser.tokens.TokenType.PLUS)), "PLUS")
        number_node = mathParser.nodes.NumberNode(69)
        self.assertEqual(str(number_node), "69")
        self.assertEqual(str(mathParser.nodes.StringNode("hello")), "\"hello\"")
        self.assertEqual(str(mathParser.nodes.AddNode(number_node, number_node)), "(69+69)")
        self.assertEqual(str(mathParser.nodes.SubtractNode(number_node, number_node)), "(69-69)")
        self.assertEqual(str(mathParser.nodes.MultiplyNode(number_node, number_node)), "(69*69)")
        self.assertEqual(str(mathParser.nodes.DivideNode(number_node, number_node)), "(69/69)")
        self.assertEqual(str(mathParser.nodes.ModuloNode(number_node, number_node)), "(69%69)")
        self.assertEqual(str(mathParser.nodes.PowerNode(number_node, number_node)), "(69**69)")
        self.assertEqual(str(mathParser.nodes.BWLeftShiftNode(number_node, number_node)), "(69 << 69)")
        self.assertEqual(str(mathParser.nodes.BWRightShiftNode(number_node, number_node)), "(69 >> 69)")
        self.assertEqual(str(mathParser.nodes.BWOrNode(number_node, number_node)), "(69 | 69)")
        self.assertEqual(str(mathParser.nodes.BWAndNode(number_node, number_node)), "(69 & 69)")
        self.assertEqual(str(mathParser.nodes.BWXorNode(number_node, number_node)), "(69 ^ 69)")
        self.assertEqual(str(mathParser.nodes.BWNotNode(number_node)), "(~69)")
        self.assertEqual(str(mathParser.nodes.PlusNode(number_node)), "(+69)")
        self.assertEqual(str(mathParser.nodes.MinusNode(number_node)), "(-69)")
        self.assertEqual(processor.execute(""), None)
        self.assertEqual(processor.execute("2 >> "), "InvalidSyntax: Incomplete math expression.")
        self.assertEqual(processor.execute("1 + 1 // comment"), 2)

    def test_variable(self):
        self.assertEqual(processor.execute("int a = 10"), None)
        self.assertEqual(processor.execute("print (a)"), "10")
        self.assertEqual(processor.execute("a + 20"), 30)
        self.assertEqual(processor.execute("a = 20"), None)
        self.assertEqual(processor.execute("print (a)"), "20")
        self.assertEqual(processor.execute("a += 10"), None)
        self.assertEqual(processor.execute("print (a)"), "30")
        self.assertEqual(processor.execute("a -= 20"), None)
        self.assertEqual(processor.execute("print (a)"), "10")
        self.assertEqual(processor.execute("a *= 10"), None)
        self.assertEqual(processor.execute("print (a)"), "100")
        self.assertEqual(processor.execute("a /= 10"), None)
        self.assertEqual(processor.execute("print (a)"), "10")
        self.assertEqual(processor.execute("a %= 2"), None)
        self.assertEqual(processor.execute("print (a)"), "0")
        self.assertEqual(processor.execute("a = 10"), None)
        self.assertEqual(processor.execute("a %= 3"), None)
        self.assertEqual(processor.execute("print (a)"), "1")
        self.assertEqual(processor.execute("del a"), None)
        self.assertEqual(
            processor.execute("print (a)"),
            'InvalidSyntax: Unknown character "a" in Math expression at character 1 in expression "a ".',
        )
        self.assertEqual(processor.execute("bool f = true"), None)
        self.assertEqual(processor.execute('dynamic g = new Dynamic ("h")'), None)
        self.assertEqual(processor.execute('g = new Dynamic ("**h**")'), None)

    def test_input(self):
        with open("inputsim.txt", "w") as f:
            f.writelines(["This file is used for Simulating user input.\n"])
        sys.stdin = open("inputsim.txt", "r")
        self.assertEqual(processor.execute("string e = input ()"), None)
        self.assertEqual(
            processor.execute("print (e)"),
            "This file is used for Simulating user input.",
        )
        sys.stdin.close()
        sys.stdin = sys.__stdin__

    def test_loopfor(self):
        self.assertEqual(processor.execute('loopfor 5 print ("tong") end'), None)

    def test_if_else(self):
        self.assertEqual(processor.execute("int b = 10"), None)
        self.assertEqual(
            processor.execute('if b == 10 then print ("b is equal to 10") end'), None
        )

    def test_switch_case(self):
        self.assertEqual(processor.execute("float c = 20.0"), None)
        self.assertEqual(
            processor.execute(
                'switch c case 10.0 print ("The value of c is 10") break case 20.0 print ("The value of c is 20.") break end'
            ),
            None,
        )

    def test_ternary_operator(self):
        self.assertEqual(processor.execute("int d = 10"), None)
        self.assertEqual(
            processor.execute(
                '? d >= 10 : print ("a is more than or equal to 10") : print ("a is less than 10") :'
            ),
            None,
        )

    def test_parse_file(self):
        with open("inputsim.txt", "w") as f:
            f.write("Hello there\ne\none\ncontinue")
        sys.stdin = open("inputsim.txt", "r")
        processor.FileProcessor().parse_file("main.sts", "inputsim.txt", True)
        processor.STORYSCRIPT_INTERPRETER_DEBUG_MODE = False
        processor.FileProcessor().parse_file("main.sts", "inputsim.txt", True)
        self.assertEqual(processor.FileProcessor().parse_file("", "inputsim.txt"), None)
        with open("test.sts", "w") as f:
            f.writelines(["var a = 10\n", 'print ("Hello there!")\n'])
        self.assertEqual(
            processor.FileProcessor().parse_file("test.sts", None, True),
            ["Hello there!"],
        )
        delete_file("test.sts")
        sys.stdin.close()
        sys.stdin = sys.__stdin__

    def test_array(self):
        self.assertEqual(processor.execute("int[] arr = new int[5]"), None)
        self.assertEqual(processor.execute("float[] arr1 = new float[5]"), None)
        self.assertEqual(processor.execute("string[] arr2 = new string[5]"), None)
        self.assertEqual(processor.execute("dynamic[] arr3 = new dynamic[5]"), None)
        self.assertEqual(processor.execute("bool[] arr4 = new bool[5]"), None)
        self.assertEqual(processor.execute("arr.Set(1, value=2)"), None)
        self.assertEqual(processor.execute("arr.AddOnIndex(2, value=3)"), None)
        self.assertTrue((processor.execute("arr").data == np.array([0, 2, 3, 0, 0])).all())


if __name__ == "__main__":
    unittest.main()
