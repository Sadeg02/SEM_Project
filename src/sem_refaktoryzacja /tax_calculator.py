from functions.initialization import initialization_of_tax_calculator

import settings

class TaxCalculator(object):

    def __init__(self, income=None, contract_type=None, auto_calculate=True):
        # Initialize all instance variables
        self.gross_income = 0
        self.contract_type = ""
        self.social_security_contribution = 0
        self.health_social_security_contribution = 0
        self.sickness_social_security_contribution = 0
        self.deductible_expenses = settings.EMPLOYMENT_FIXED_DEDUCTIBLE
        self.health_insurance_contribution = 0
        self.health_insurance_deductible = 0
        self.advance_tax_base = 0
        self.advance_tax = 0
        self.advance_tax_rounded = 0
        self.net_income = 0

        # Initialize income and contract type
        initialization_of_tax_calculator(self, income, contract_type)

        # Automatically run calculations if requested (default behavior)
        if auto_calculate:
            self.calculate()

    def calculate(self):
        if self.contract_type == settings.CONTRACT_TYPE_EMPLOYMENT:
            self._calculate_employment_contract()
        elif self.contract_type == settings.CONTRACT_TYPE_CIVIL:
            self._calculate_civil_contract()
        else:
            raise ValueError(f"Unknown contract type: {self.contract_type}")

    def _calculate_employment_contract(self):
        # Calculate taxes for employment contract
        # Calculate social security contributions
        income_after_social_security = self.calculate_income_after_social_security(self.gross_income)

        # Calculate health insurance
        self.calculate_health_insurance(income_after_social_security)

        # Deductible expenses are fixed for employment contracts
        # (already set in __init__)

        # Calculate taxable income
        taxable_income = income_after_social_security - self.deductible_expenses
        taxable_income_rounded = float("{0:.0f}".format(taxable_income))

        # Calculate advance tax
        self.calculate_advance_tax_base(taxable_income_rounded)
        self.calculate_advance_tax()
        self.advance_tax_rounded = float("{0:.0f}".format(self.advance_tax))

        # Calculate net income
        net_income_calculated = self.gross_income - (
            (self.social_security_contribution +
             self.health_social_security_contribution +
             self.sickness_social_security_contribution) +
            self.health_insurance_contribution +
            self.advance_tax_rounded
        )
        self.net_income = float("{0:.2f}".format(net_income_calculated))

    def _calculate_civil_contract(self):
        # Calculate taxes for civil contract
        # Calculate social security contributions
        income_after_social_security = self.calculate_income_after_social_security(self.gross_income)

        # Calculate health insurance
        self.calculate_health_insurance(income_after_social_security)

        # For civil contracts, no tax-free amount and different deductible expenses
        settings.REDUCED_TAX = 0
        self.deductible_expenses = income_after_social_security * settings.DEDUCTIBLE_EXPENSES[settings.CONTRACT_TYPE_CIVIL]

        # Calculate taxable income
        taxable_income = income_after_social_security - self.deductible_expenses
        taxable_income_rounded = float("{0:.0f}".format(taxable_income))

        # Calculate advance tax
        self.calculate_advance_tax_base(taxable_income_rounded)
        self.calculate_advance_tax()
        self.advance_tax_rounded = float("{0:.0f}".format(self.advance_tax))

        # Calculate net income
        net_income_calculated = self.gross_income - (
            (self.social_security_contribution +
             self.health_social_security_contribution +
             self.sickness_social_security_contribution) +
            self.health_insurance_contribution +
            self.advance_tax_rounded
        )
        self.net_income = float("{0:.2f}".format(net_income_calculated))

    def calculate_advance_tax(self):
        self.advance_tax = self.advance_tax_base - self.health_insurance_deductible - settings.REDUCED_TAX

    def calculate_advance_tax_base(self, income):
        self.advance_tax_base = income * settings.TAX_RATE

    def calculate_income_after_social_security(self, income):
        self.social_security_contribution = income * settings.SOCIAL_SECURITY_RATE
        self.health_social_security_contribution = income * settings.HEALTH_SECURITY_RATE
        self.sickness_social_security_contribution = income * settings.SICKNESS_SECURITY_RATE
        return (income - self.social_security_contribution - self.health_social_security_contribution - self.sickness_social_security_contribution)

    def calculate_health_insurance(self, income):
        self.health_insurance_contribution = income * settings.HEALTH_INSURANCE_RATE_PRIMARY
        self.health_insurance_deductible = income * settings.HEALTH_INSURANCE_RATE_FROM_TAX
