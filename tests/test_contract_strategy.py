import sys
import os
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULE_DIR = os.path.join(ROOT, 'src', 'sem_refaktoryzacja ')
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from contracts.contract_strategy import (
    ContractStrategyFactory,
    ContractStrategy,
    EmploymentContractStrategy,
    CivilContractStrategy
)
import settings


class TestContractStrategyFactory(unittest.TestCase):

    def test_create_employment_strategy(self):
        strategy = ContractStrategyFactory.create_strategy(settings.CONTRACT_TYPE_EMPLOYMENT)
        self.assertIsInstance(strategy, EmploymentContractStrategy)

    def test_create_civil_strategy(self):
        strategy = ContractStrategyFactory.create_strategy(settings.CONTRACT_TYPE_CIVIL)
        self.assertIsInstance(strategy, CivilContractStrategy)

    def test_create_invalid_strategy_raises_error(self):
        with self.assertRaises(ValueError) as context:
            ContractStrategyFactory.create_strategy("INVALID")
        self.assertIn("Unknown contract type", str(context.exception))


class TestEmploymentContractStrategy(unittest.TestCase):

    def setUp(self):
        # Reset to default settings before each test for isolation
        settings.REDUCED_TAX = {
            settings.CONTRACT_TYPE_EMPLOYMENT: 46.33,
            settings.CONTRACT_TYPE_CIVIL: 0.0
        }
        self.strategy = EmploymentContractStrategy()

    def test_get_contract_type(self):
        self.assertEqual(self.strategy.get_contract_type(), settings.CONTRACT_TYPE_EMPLOYMENT)

    def test_calculate_deductible_expenses_returns_fixed_amount(self):
        income = 1000.0
        result = self.strategy.calculate_deductible_expenses(income)
        self.assertEqual(result, settings.EMPLOYMENT_FIXED_DEDUCTIBLE)
        self.assertEqual(result, 111.25)

    def test_deductible_expenses_independent_of_income(self):
        result_1000 = self.strategy.calculate_deductible_expenses(1000)
        result_5000 = self.strategy.calculate_deductible_expenses(5000)
        self.assertEqual(result_1000, result_5000)

    def test_get_reduced_tax_amount(self):
        result = self.strategy.get_reduced_tax_amount()
        self.assertEqual(result, 46.33)

    def test_get_reduced_tax_uses_settings(self):
        # Test with custom value to verify strategy reads from settings
        settings.REDUCED_TAX = {
            settings.CONTRACT_TYPE_EMPLOYMENT: 50.0,
            settings.CONTRACT_TYPE_CIVIL: 0.0
        }
        result = self.strategy.get_reduced_tax_amount()
        self.assertEqual(result, 50.0)


class TestCivilContractStrategy(unittest.TestCase):

    def setUp(self):
        # Reset to default settings before each test for isolation
        settings.REDUCED_TAX = {
            settings.CONTRACT_TYPE_EMPLOYMENT: 46.33,
            settings.CONTRACT_TYPE_CIVIL: 0.0
        }
        self.strategy = CivilContractStrategy()

    def test_get_contract_type(self):
        self.assertEqual(self.strategy.get_contract_type(), settings.CONTRACT_TYPE_CIVIL)

    def test_calculate_deductible_expenses_is_percentage(self):
        income = 1000.0
        result = self.strategy.calculate_deductible_expenses(income)
        expected = 1000.0 * 0.2
        self.assertEqual(result, expected)

    def test_calculate_deductible_expenses_scales_with_income(self):
        income_1000 = 1000.0
        income_2000 = 2000.0

        result_1000 = self.strategy.calculate_deductible_expenses(income_1000)
        result_2000 = self.strategy.calculate_deductible_expenses(income_2000)

        self.assertEqual(result_2000, result_1000 * 2)

    def test_calculate_deductible_expenses_uses_settings_rate(self):
        income = 862.9
        result = self.strategy.calculate_deductible_expenses(income)
        expected = 862.9 * settings.DEDUCTIBLE_EXPENSES[settings.CONTRACT_TYPE_CIVIL]
        self.assertAlmostEqual(result, expected, places=2)

    def test_get_reduced_tax_amount_is_zero(self):
        result = self.strategy.get_reduced_tax_amount()
        self.assertEqual(result, 0.0)

    def test_reduced_tax_zero_regardless_of_settings(self):
        # Test that civil always returns 0 even if employment has different value
        settings.REDUCED_TAX = {
            settings.CONTRACT_TYPE_EMPLOYMENT: 100.0,
            settings.CONTRACT_TYPE_CIVIL: 0.0
        }
        result = self.strategy.get_reduced_tax_amount()
        self.assertEqual(result, 0.0)


class TestContractStrategyInterface(unittest.TestCase):

    def test_base_strategy_methods_raise_not_implemented(self):
        strategy = ContractStrategy()

        with self.assertRaises(NotImplementedError):
            strategy.get_contract_type()

        with self.assertRaises(NotImplementedError):
            strategy.calculate_deductible_expenses(1000)

        with self.assertRaises(NotImplementedError):
            strategy.get_reduced_tax_amount()


class TestStrategyIntegration(unittest.TestCase):

    def setUp(self):
        # Reset to default settings before each test for isolation
        settings.REDUCED_TAX = {
            settings.CONTRACT_TYPE_EMPLOYMENT: 46.33,
            settings.CONTRACT_TYPE_CIVIL: 0.0
        }

    def test_employment_and_civil_produce_different_deductibles(self):
        income = 862.9
        employment = EmploymentContractStrategy()
        civil = CivilContractStrategy()

        emp_deductible = employment.calculate_deductible_expenses(income)
        civ_deductible = civil.calculate_deductible_expenses(income)

        self.assertNotEqual(emp_deductible, civ_deductible)
        self.assertEqual(emp_deductible, 111.25)
        self.assertAlmostEqual(civ_deductible, 172.58, places=2)

    def test_employment_and_civil_produce_different_reduced_tax(self):
        # Uses default settings - no need to set REDUCED_TAX
        employment = EmploymentContractStrategy()
        civil = CivilContractStrategy()

        emp_reduced = employment.get_reduced_tax_amount()
        civ_reduced = civil.get_reduced_tax_amount()

        self.assertNotEqual(emp_reduced, civ_reduced)
        self.assertEqual(emp_reduced, 46.33)
        self.assertEqual(civ_reduced, 0.0)


if __name__ == '__main__':
    unittest.main()
