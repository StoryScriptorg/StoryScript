""" TESTING CASES """
import unittest
import processor
from os import remove as delete_file
import sys


class TestReturnedValue(unittest.TestCase):
    def test_arithmatics(self):
        self.assertEqual(processor.execute("// Arithmatics test"), None)
        self.assertEqual(processor.execute("5 + 5 * 0"), 5)
        self.assertEqual(processor.execute("10 + 20 * 2"), 50)

    def test_exceptions(self):
        self.assertEqual(
            processor.execute("throw DivideByZeroException"),
            "DivideByZeroException: You cannot divide numbers with 0",
        )
        self.assertEqual(
            processor.execute("throw InvalidValue Description"),
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
                "throw NotImplementedException This feature is in Alpha. Please add a Alpha tester profile to use this Feature."
            ),
            "NotImplementedException: This feature is in Alpha. Please add a Alpha tester profile to use this Feature.",
        )
        self.assertEqual(
            processor.execute("throw DivideByZeroException"),
            "DivideByZeroException: You cannot divide numbers with 0",
        )
        self.assertEqual(
            processor.execute(
                "throw InvalidTypeException The input type cannot be an Iterable data."
            ),
            "InvalidTypeException: The input type cannot be an Iterable data.",
        )

    def test_variable(self):
        self.assertEqual(processor.execute("int a = 10"), None)
        self.assertEqual(processor.execute("print (a)"), "10")
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
            'InvalidSyntax: Unknown character "a" in Math expression.',
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
            f.writelines(["Hello there\n"])
        sys.stdin = open("inputsim.txt", "r")
        try:
            processor.parse_file("main.sts", "inputsim.txt", True), ["40"]
        except SystemExit:
            pass
        self.assertEqual(processor.parse_file("", "inputsim.txt"), None)
        with open("test.sts", "w") as f:
            f.writelines(["var a = 10\n", 'print ("Hello there!")\n'])
        self.assertEqual(processor.parse_file("test.sts", None, True), ["Hello there!"])
        delete_file("test.sts")
        sys.stdin.close()
        sys.stdin = sys.__stdin__


if __name__ == "__main__":
    unittest.main()
