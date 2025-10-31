import sys
import os
import unittest
from io import StringIO

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULE_DIR = os.path.join(ROOT, 'src', 'sem_refaktoryzacja ')
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from presenters.tax_result_printer import (
    TaxResultPrinter,
    EmploymentPrintStrategy,
    CivilPrintStrategy
)
from tax_calculator import TaxCalculator
import settings


class TestTaxResultPrinter(unittest.TestCase):

    def setUp(self):
        self.printer = TaxResultPrinter()
        settings.REDUCED_TAX = 46.33

    def test_format_currency_with_decimals(self):
        result = self.printer._format_currency(1234.56)
        self.assertEqual(result, "1234.56")

    def test_format_currency_rounds_to_two_decimals(self):
        result = self.printer._format_currency(1234.567)
        self.assertEqual(result, "1234.57")

    def test_format_rounded_removes_decimals(self):
        result = self.printer._format_rounded(1234.99)
        self.assertEqual(result, "1235")

    def test_calculate_income_after_social_security(self):
        calc = TaxCalculator(income=1000, contract_type='E')
        result = self.printer._calculate_income_after_social_security(calc)
        expected = 1000 - 97.6 - 15.0 - 24.5
        self.assertAlmostEqual(result, expected, places=2)


class TestEmploymentPrintStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = EmploymentPrintStrategy()
        self.printer = TaxResultPrinter()
        settings.REDUCED_TAX = 46.33

    def test_get_contract_name(self):
        self.assertEqual(self.strategy.get_contract_name(), "EMPLOYMENT")

    def test_print_tax_details_includes_tax_free_income(self):
        calc = TaxCalculator(income=1000, contract_type='E')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.strategy.print_tax_details(calc, self.printer)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Tax free income", output)
        self.assertIn("46.33", output)
        self.assertIn("Reduced tax", output)


class TestCivilPrintStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = CivilPrintStrategy()
        self.printer = TaxResultPrinter()
        settings.REDUCED_TAX = 46.33

    def test_get_contract_name(self):
        self.assertEqual(self.strategy.get_contract_name(), "CIVIL")

    def test_print_tax_details_shows_already_paid_tax(self):
        calc = TaxCalculator(income=1000, contract_type='C')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.strategy.print_tax_details(calc, self.printer)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Already paid tax", output)
        self.assertNotIn("Tax free income", output)


class TestPrinterOutput(unittest.TestCase):

    def setUp(self):
        self.printer = TaxResultPrinter()
        settings.REDUCED_TAX = 46.33

    def test_employment_contract_output_contains_key_sections(self):
        calc = TaxCalculator(income=1000, contract_type='E')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.printer.print_results(calc)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("EMPLOYMENT", output)
        self.assertIn("Income 1000.00", output)
        self.assertIn("Social security tax", output)
        self.assertIn("Health social security tax", output)
        self.assertIn("Sickness social security tax", output)
        self.assertIn("Tax deductible expenses", output)
        self.assertIn("Net income = 763.24", output)

    def test_civil_contract_output_contains_key_sections(self):
        calc = TaxCalculator(income=1000, contract_type='C')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.printer.print_results(calc)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("CIVIL", output)
        self.assertIn("Income 1000.00", output)
        self.assertIn("Social security tax", output)
        self.assertIn("Tax deductible expenses", output)
        self.assertIn("Net income = 728.24", output)
        self.assertIn("Already paid tax", output)

    def test_print_results_for_different_incomes(self):
        calc_2000 = TaxCalculator(income=2000, contract_type='E')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.printer.print_results(calc_2000)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Income 2000.00", output)
        self.assertIn("Net income", output)

    def test_section_printing_methods_work_independently(self):
        calc = TaxCalculator(income=1000, contract_type='E')

        captured_output = StringIO()
        sys.stdout = captured_output
        self.printer._print_section_header("TEST")
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "TEST")

        captured_output = StringIO()
        sys.stdout = captured_output
        self.printer._print_gross_income(calc)
        sys.stdout = sys.__stdout__
        self.assertIn("Income 1000.00", captured_output.getvalue())

    def test_printer_handles_zero_income(self):
        calc = TaxCalculator(income=0, contract_type='E')
        captured_output = StringIO()
        sys.stdout = captured_output

        self.printer.print_results(calc)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Income 0.00", output)
        self.assertIn("Net income", output)


if __name__ == '__main__':
    unittest.main()
