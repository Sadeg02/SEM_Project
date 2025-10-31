from functions.initialization import initialization_of_tax_calculator

import settings

class TaxCalculator(object):

    def __init__(self, income=None, contract_type=None):
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
        #After initialization, run the main logic
        self.main_logic()

    def main_logic(self):
        if self.contract_type == settings.CONTRACT_TYPE_EMPLOYMENT:
            print("EMPLOYMENT")
            print("Income ", self.gross_income)
            income_after_social_security = self.calculate_income_after_social_security(self.gross_income)
            print("Social security tax: "+"{0:.2f}".format(self.social_security_contribution))
            print("Health social security tax: "+"{0:.2f}".format(self.health_social_security_contribution))
            print("Sickness social security tax: "+"{0:.2f}".format(self.sickness_social_security_contribution))
            print("Income basis for healt social security: ", income_after_social_security)
            self.calculate_health_insurance(income_after_social_security)
            print("Healt social security tax: 9% = " \
                  + "{0:.2f}".format(self.health_insurance_contribution) + " 7,75% = " +
                  "{0:.2f}".format(self.health_insurance_deductible))
            print("Tax deductible expenses: ", self.deductible_expenses)
            taxable_income = income_after_social_security - self.deductible_expenses
            taxable_income_rounded = float("{0:.0f}".format(taxable_income))
            print("Income: ", taxable_income, " rounded: " + "{0:.0f}".format(taxable_income_rounded))
            self.calculate_advance_tax_base(taxable_income_rounded)
            print("Advance tax 18% = ", self.advance_tax_base)
            print("Tax free income =", settings.REDUCED_TAX)
            reduced_tax = self.advance_tax_base - settings.REDUCED_TAX
            print("Reduced tax = " + "{0:.2f}".format(reduced_tax))
            self.calculate_advance_tax()
            self.advance_tax_rounded = float("{0:.0f}".format(self.advance_tax))
            print("Advance paid tax = " + "{0:.2f}".format(self.advance_tax) +
                  " rounded " + "{0:.0f}".format(self.advance_tax_rounded))
            net_income_calculated = self.gross_income - ((self.social_security_contribution + self.health_social_security_contribution
                                                 + self.sickness_social_security_contribution) + self.health_insurance_contribution + self.advance_tax_rounded)
            # store computed net income for external use/tests
            self.net_income = float("{0:.2f}".format(net_income_calculated))
            print()
            print("Net income = " + "{0:.2f}".format(net_income_calculated))

        elif self.contract_type == settings.CONTRACT_TYPE_CIVIL:
            print("CIVIL")
            print("Income", self.gross_income)
            income_after_social_security = self.calculate_income_after_social_security(self.gross_income)
            print("Social security tax: " + "{0:.2f}".format(self.social_security_contribution))
            print("Health social security tax: " + "{0:.2f}".format(self.health_social_security_contribution))
            print("Sickness social security tax  " + "{0:.2f}".format(self.sickness_social_security_contribution))
            print("Income for calculating health security tax: ", income_after_social_security)
            self.calculate_health_insurance(income_after_social_security)
            print("Health security tax: 9% = " \
                  + "{0:.2f}".format(self.health_insurance_contribution) + " 7,75% = " +
                  "{0:.2f}".format(self.health_insurance_deductible))
            settings.REDUCED_TAX = 0
            self.deductible_expenses = income_after_social_security * settings.DEDUCTIBLE_EXPENSES["C"]
            print("Tax deductible expenses = ", self.deductible_expenses)
            taxable_income = income_after_social_security - self.deductible_expenses
            taxable_income_rounded = float("{0:.0f}".format(taxable_income))
            print("income to be taxed: ", taxable_income, " rounded: " + "{0:.0f}".format(taxable_income_rounded))
            self.calculate_advance_tax_base(taxable_income_rounded)
            print("Advance tax 18% =", self.advance_tax_base)
            print("Already paid tax = " + "{0:.2f}".format(self.advance_tax_base))
            self.calculate_advance_tax()
            self.advance_tax_rounded = float("{0:.0f}".format(self.advance_tax))
            print("Advance tax = " + "{0:.2f}".format(self.advance_tax) +
                  " rounded " + "{0:.0f}".format(self.advance_tax_rounded))
            net_income_calculated = self.gross_income - ((self.social_security_contribution + self.health_social_security_contribution
                                                 + self.sickness_social_security_contribution) + self.health_insurance_contribution + self.advance_tax_rounded)
            # store computed net income for external use/tests
            self.net_income = float("{0:.2f}".format(net_income_calculated))
            print()
            print("Net income = " + "{0:.2f}".format(net_income_calculated))
        else:
            print("Unknown type of contract!")

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
