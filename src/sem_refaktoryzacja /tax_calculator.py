from functions.initialization import initialization_of_tax_calculator
from contracts.contract_strategy import ContractStrategyFactory

import settings


class TaxCalculator(object):
    # Tax calculator using Strategy pattern for contract-specific rules

    def __init__(self, income=None, contract_type=None, auto_calculate=True):
        # Initialize all instance variables
        self.gross_income = 0
        self.contract_type = ""
        self.social_security_contribution = 0
        self.health_social_security_contribution = 0
        self.sickness_social_security_contribution = 0
        self.deductible_expenses = 0
        self.health_insurance_contribution = 0
        self.health_insurance_deductible = 0
        self.advance_tax_base = 0
        self.advance_tax = 0
        self.advance_tax_rounded = 0
        self.net_income = 0
        self.contract_strategy = None

        # Initialize income and contract type
        initialization_of_tax_calculator(self, income, contract_type)

        # Create appropriate strategy based on contract type
        self.contract_strategy = ContractStrategyFactory.create_strategy(self.contract_type)

        # Automatically run calculations if requested (default behavior)
        if auto_calculate:
            self.calculate()

    def calculate(self):
        # Main calculation flow - Template Method using strategy for contract-specific rules
        income_after_social = self._calculate_social_security_deductions()
        self._calculate_health_insurance(income_after_social)
        self._calculate_deductible_expenses(income_after_social)
        taxable_income_rounded = self._calculate_taxable_income(income_after_social)
        self._calculate_taxes(taxable_income_rounded)
        self._calculate_net_income()

    # Step 1: Social Security Deductions
    def _calculate_social_security_deductions(self):
        # Calculate all social security contributions and return income after deductions
        self.social_security_contribution = self._apply_rate(
            self.gross_income,
            settings.SOCIAL_SECURITY_RATE
        )
        self.health_social_security_contribution = self._apply_rate(
            self.gross_income,
            settings.HEALTH_SECURITY_RATE
        )
        self.sickness_social_security_contribution = self._apply_rate(
            self.gross_income,
            settings.SICKNESS_SECURITY_RATE
        )

        return self._get_income_after_social_security()

    def _get_income_after_social_security(self):
        # Calculate income remaining after all social security deductions
        return (self.gross_income -
                self.social_security_contribution -
                self.health_social_security_contribution -
                self.sickness_social_security_contribution)

    # Step 2: Health Insurance
    def _calculate_health_insurance(self, income_basis):
        # Calculate health insurance contributions based on income after social security
        self.health_insurance_contribution = self._apply_rate(
            income_basis,
            settings.HEALTH_INSURANCE_RATE_PRIMARY
        )
        self.health_insurance_deductible = self._apply_rate(
            income_basis,
            settings.HEALTH_INSURANCE_RATE_FROM_TAX
        )

    # Step 3: Deductible Expenses (contract-specific)
    def _calculate_deductible_expenses(self, income_after_social):
        # Use strategy to calculate contract-specific deductible expenses
        self.deductible_expenses = self.contract_strategy.calculate_deductible_expenses(
            income_after_social
        )

    # Step 4: Taxable Income
    def _calculate_taxable_income(self, income_after_social):
        # Calculate income subject to tax and round to whole number
        taxable_income = income_after_social - self.deductible_expenses
        return self._round_to_integer(taxable_income)

    # Step 5: Tax Calculations
    def _calculate_taxes(self, taxable_income_rounded):
        # Calculate advance tax base and final advance tax
        self._calculate_advance_tax_base(taxable_income_rounded)
        self._calculate_advance_tax()
        self.advance_tax_rounded = self._round_to_integer(self.advance_tax)

    def _calculate_advance_tax_base(self, taxable_income):
        # Calculate base tax amount (18% of taxable income)
        self.advance_tax_base = self._apply_rate(taxable_income, settings.TAX_RATE)

    def _calculate_advance_tax(self):
        # Calculate final advance tax after deductions (contract-specific)
        reduced_tax = self.contract_strategy.get_reduced_tax_amount()
        self.advance_tax = (self.advance_tax_base -
                           self.health_insurance_deductible -
                           reduced_tax)

    # Step 6: Net Income
    def _calculate_net_income(self):
        # Calculate final net income after all deductions
        total_social_security = self._get_total_social_security()
        total_deductions = (total_social_security +
                           self.health_insurance_contribution +
                           self.advance_tax_rounded)

        net_income_calculated = self.gross_income - total_deductions
        self.net_income = self._round_to_currency(net_income_calculated)

    def _get_total_social_security(self):
        # Sum all social security contributions
        return (self.social_security_contribution +
                self.health_social_security_contribution +
                self.sickness_social_security_contribution)

    # Utility Methods - Single Responsibility
    def _apply_rate(self, amount, rate):
        # Apply a percentage rate to an amount
        return amount * rate

    def _round_to_integer(self, amount):
        # Round amount to nearest integer
        return float("{0:.0f}".format(amount))

    def _round_to_currency(self, amount):
        # Round amount to 2 decimal places (currency format)
        return float("{0:.2f}".format(amount))
