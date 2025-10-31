import sys
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULE_DIR = os.path.join(ROOT, 'src', 'tax_calculator')
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from strategies.contract_strategy import (
    ContractStrategyFactory,
    ContractStrategy,
    EmploymentContractStrategy,
    CivilContractStrategy
)
from tax_settings import TaxSettings


class TestContractStrategyFactory(unittest.TestCase):

    def test_create_employment_strategy(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = ContractStrategyFactory.create_strategy(calc.settings.contract_type_employment, calc)
        self.assertIsInstance(strategy, EmploymentContractStrategy)

    def test_create_civil_strategy(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = ContractStrategyFactory.create_strategy(calc.settings.contract_type_civil, calc)
        self.assertIsInstance(strategy, CivilContractStrategy)

    def test_create_invalid_strategy_raises_error(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        with self.assertRaises(ValueError) as context:
            ContractStrategyFactory.create_strategy("INVALID", calc)
        self.assertIn("Unknown contract type", str(context.exception))


class TestEmploymentContractStrategy(unittest.TestCase):

    def test_get_contract_type(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = EmploymentContractStrategy(calc)
        self.assertEqual(strategy.get_contract_type(), calc.settings.contract_type_employment)

    def test_calculate_deductible_expenses_returns_fixed_amount(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = EmploymentContractStrategy(calc)
        income = 1000.0
        result = strategy.calculate_deductible_expenses(income)
        self.assertEqual(result, calc.settings.employment_fixed_deductible)
        self.assertEqual(result, 111.25)

    def test_deductible_expenses_independent_of_income(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = EmploymentContractStrategy(calc)
        result_1000 = strategy.calculate_deductible_expenses(1000)
        result_5000 = strategy.calculate_deductible_expenses(5000)
        self.assertEqual(result_1000, result_5000)

    def test_get_reduced_tax_amount(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = EmploymentContractStrategy(calc)
        result = strategy.get_reduced_tax_amount()
        self.assertEqual(result, 46.33)

    def test_get_reduced_tax_uses_settings(self):
        # Test with custom value to verify strategy reads from calculator's settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()
                # Modify this calculator's settings
                self.settings.reduced_tax = {
                    self.settings.contract_type_employment: 50.0,
                    self.settings.contract_type_civil: 0.0
                }

        calc = MockCalculator()
        strategy = EmploymentContractStrategy(calc)
        result = strategy.get_reduced_tax_amount()
        self.assertEqual(result, 50.0)


class TestCivilContractStrategy(unittest.TestCase):

    def test_get_contract_type(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        self.assertEqual(strategy.get_contract_type(), calc.settings.contract_type_civil)

    def test_calculate_deductible_expenses_is_percentage(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        income = 1000.0
        result = strategy.calculate_deductible_expenses(income)
        expected = 1000.0 * 0.2
        self.assertEqual(result, expected)

    def test_calculate_deductible_expenses_scales_with_income(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        income_1000 = 1000.0
        income_2000 = 2000.0

        result_1000 = strategy.calculate_deductible_expenses(income_1000)
        result_2000 = strategy.calculate_deductible_expenses(income_2000)

        self.assertEqual(result_2000, result_1000 * 2)

    def test_calculate_deductible_expenses_uses_settings_rate(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        income = 862.9
        result = strategy.calculate_deductible_expenses(income)
        contract_type = calc.settings.contract_type_civil
        expected = 862.9 * calc.settings.deductible_expenses[contract_type]
        self.assertAlmostEqual(result, expected, places=2)

    def test_get_reduced_tax_amount_is_zero(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        result = strategy.get_reduced_tax_amount()
        self.assertEqual(result, 0.0)

    def test_reduced_tax_zero_regardless_of_settings(self):
        # Test that civil always returns 0 even if employment has different value
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()
                # Modify employment value but civil should still be 0
                self.settings.reduced_tax = {
                    self.settings.contract_type_employment: 100.0,
                    self.settings.contract_type_civil: 0.0
                }

        calc = MockCalculator()
        strategy = CivilContractStrategy(calc)
        result = strategy.get_reduced_tax_amount()
        self.assertEqual(result, 0.0)


class TestContractStrategyInterface(unittest.TestCase):

    def test_base_strategy_methods_raise_not_implemented(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        strategy = ContractStrategy(calc)

        with self.assertRaises(NotImplementedError):
            strategy.get_contract_type()

        with self.assertRaises(NotImplementedError):
            strategy.calculate_deductible_expenses(1000)

        with self.assertRaises(NotImplementedError):
            strategy.get_reduced_tax_amount()


class TestStrategyIntegration(unittest.TestCase):

    def test_employment_and_civil_produce_different_deductibles(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        income = 862.9
        employment = EmploymentContractStrategy(calc)
        civil = CivilContractStrategy(calc)

        emp_deductible = employment.calculate_deductible_expenses(income)
        civ_deductible = civil.calculate_deductible_expenses(income)

        self.assertNotEqual(emp_deductible, civ_deductible)
        self.assertEqual(emp_deductible, 111.25)
        self.assertAlmostEqual(civ_deductible, 172.58, places=2)

    def test_employment_and_civil_produce_different_reduced_tax(self):
        # Create a mock calculator with settings
        class MockCalculator:
            def __init__(self):
                self.settings = TaxSettings.default()

        calc = MockCalculator()
        employment = EmploymentContractStrategy(calc)
        civil = CivilContractStrategy(calc)

        emp_reduced = employment.get_reduced_tax_amount()
        civ_reduced = civil.get_reduced_tax_amount()

        self.assertNotEqual(emp_reduced, civ_reduced)
        self.assertEqual(emp_reduced, 46.33)
        self.assertEqual(civ_reduced, 0.0)


if __name__ == '__main__':
    unittest.main()
