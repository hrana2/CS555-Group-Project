import unittest
from gedcom_parser import test_us02_birth_b4_marriage, test_us03_birth_b4_death, test_us04_marr_b4_divorce, test_us05_marr_b4_death, test_us06_div_b4_death, test_us07_less_than_150, test_us08_birth_b4_marr_parents, test_us09_birth_b4_death_parents


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def test_us02(self): 
        self.assertEqual(test_us02_birth_b4_marriage(), "Error: Family: @F2@: US02: Birth before married 8 SEP 2020")

    def test_03(self): 
        self.assertEqual(test_us03_birth_b4_death(), "Error: Indi: @I4@ US03: Death 1 NOV 2001 before Birthday 28 MAR 1800")

    def test_us04(self): 
        self.assertEqual(test_us04_marr_b4_divorce(), "Error: Family: @F3@: US04: Divorced 3 FEB 1995 before married 6 AUG 1995")

    def test_us05(self):
        self.assertEqual(test_us05_marr_b4_death(), "Error: Family: @F2@: US05: Death of husband before married 8 SEP 2020")
        
    def test_us06(self):
        self.assertEqual(test_us06_div_b4_death(), "Error: Family: @F5@: US06: Died before divorce 2 FEB 2020")

    def test_us07(self):
        self.assertEqual(test_us07_less_than_150(), "Error: Individual: @I4@: US07: Over 150 years old")

    def test_us08(self):
        self.assertEqual(test_us08_birth_b4_marr_parents(), "Error: Individual: @I2@: US08: born after marriage of parents")

    def test_us09(self):
        self.assertEqual(test_us09_birth_b4_death_parents(), "Error: Individual: @I9@: US09 born 9 months after death of dad")
        

if __name__ == '__main__':
    unittest.main()
 




# test_us02_birth_b4_marriage()

# test_us03_birth_b4_death()

# test_us04_marr_b4_divorce()

# test_us05_marr_b4_death()
# test_us06_div_b4_death()

# test_us07_less_than_150()

# test_us08_birth_b4_marr_parents()

# test_us09_birth_b4_death_parents()



# gedcom_parser.test_us02_birth_b4_marriage()

# gedcom_parser.test_us03_birth_b4_death()


# gedcom_parser.test_us04_marr_b4_divorce()

# gedcom_parser.test_us05_marr_b4_death()
# gedcom_parser.test_us06_div_b4_death()

# gedcom_parser.test_us07_less_than_150()

# gedcom_parser.test_us08_birth_b4_marr_parents()

# gedcom_parser.test_us09_birth_b4_death_parents()