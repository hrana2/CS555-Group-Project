import unittest
import gedcom_parser

class TestStringMethods(unittest.TestCase):
    def test1(self):
        # This test is only true when using the test.ged file 
        self.assertEqual(gedcom_parser.test_us04_marr_b4_divorce(), "Error: Family: @F3@: US04: Divorced 10 JUL 2018  before married 15 JUL 2018")
        print()

if __name__ == '__main__':
    unittest.main()
