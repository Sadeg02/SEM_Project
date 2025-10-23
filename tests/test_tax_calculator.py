import sys
import os
import unittest

# Ensure the module directory is importable when running tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULE_DIR = os.path.join(ROOT, 'src', 'sem_refaktoryzacja ')
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

import tax_calculator


class TestTaxCalculator(unittest.TestCase):
    
    def test_invalid_income_input_raises(self):
        with self.assertRaises(ValueError):
            tax_calculator.TaxCalculator('coscos', 'E')
    def test_invalid_contract_type_raises(self):
        with self.assertRaises(ValueError):
            tax_calculator.TaxCalculator(1000, 'X')

    def test_zero_income_results_zero_net(self):
        tax_calculator.TaxCalculator(0, 'C')
        self.assertEqual(tax_calculator.TaxCalculator.net_income, 0.0)

    def test_negative_income_results_negative_net(self):
        tax_calculator.TaxCalculator(-1000, 'E')
        self.assertLess(tax_calculator.TaxCalculator.net_income, 0)

    def test_civil_less_than_employment_for_1000(self):
        tax_calculator.TaxCalculator(1000, 'E')
        net_e = tax_calculator.TaxCalculator.net_income
        tax_calculator.TaxCalculator(1000, 'C')
        net_c = tax_calculator.TaxCalculator.net_income
        self.assertLess(net_c, net_e)


if __name__ == '__main__':
    unittest.main()
