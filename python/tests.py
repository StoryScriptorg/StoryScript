""" TESTING CASES """
import unittest
from processor import execute

class TestReturnedValue(unittest.TestCase):
    def variable_test(self):
        self.assertEqual(execute("var a = 10"), None)
        self.assertEqual(execute("print (a)"), "10")

    def if_else_test(self):
        self.assertEqual(execute("int b = 10"), None)
        self.assertEqual(execute("if b == 10 then print (\"b is equal to 10\") end"), None)

    def switch_case_test(self):
        self.assertEqual(execute("float c = 20.0"), None)
        self.assertEqual(execute('switch c case 10.0 print ("The value of c is 10") break case 20.0 print ("The value of c is 20.") break end'), None)

if __name__ == "__main__":
    unittest.main()