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

    def test_employment_and_civil_working_for_1000(self):
        # Employment contract for 1000 PLN should give 763.24 PLN net income
        calc_e = tax_calculator.TaxCalculator(1000, 'E')
        net_e = calc_e.net_income
        self.assertEqual(net_e, 763.24)

        # Civil contract for 1000 PLN should give 728.24 PLN net income (lower due to no tax-free amount)
        calc_c = tax_calculator.TaxCalculator(1000, 'C')
        net_c = calc_c.net_income
        self.assertEqual(net_c, 728.24)

    def test_zero_income_results_zero_net(self):
        calc = tax_calculator.TaxCalculator(0, 'C')
        self.assertEqual(calc.net_income, 0.0)

    def test_negative_income_results_negative_net(self):
        calc = tax_calculator.TaxCalculator(-1000, 'E')
        self.assertLess(calc.net_income, 0)
    


if __name__ == '__main__':
    unittest.main()
