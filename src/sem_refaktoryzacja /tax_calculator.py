from functions.initialization import initialization_of_tax_calculator    

import settings

class TaxCalculator(object):
    income = 0

    contractType = ""
    t_socialSecurity = 0 
    t_socialSecurityHealth = 0
    t_socialSecuritySickness = 0

    t_deductibleExpenses = 111.25
    health_insurance_tax = 0
    health_insurance_reduce_tax = 0
    t_advance = 0
    advanceTax = 0
    advanceTax0 = 0

    def __init__(self, income=None, contractType=None):
        # Initialize income
        initialization_of_tax_calculator(TaxCalculator, income, contractType)
        #After initialization, run the main logic
        self.main_logic()

    def main_logic(self):
        if TaxCalculator.contractType == "E":
            print("EMPLOYMENT")
            print("Income ", TaxCalculator.income)
            d_income = TaxCalculator.calculateIncome(TaxCalculator.income)
            print("Social security tax: "+"{0:.2f}".format(TaxCalculator.t_socialSecurity))
            print("Health social security tax: "+"{0:.2f}".format(TaxCalculator.t_socialSecurityHealth))
            print("Sickness social security tax: "+"{0:.2f}".format(TaxCalculator.t_socialSecuritySickness))
            print("Income basis for healt social security: ", d_income)
            TaxCalculator.calculateOtherTaxes(d_income)
            print("Healt social security tax: 9% = " \
                  + "{0:.2f}".format(TaxCalculator.health_insurance_tax_rate_primary) + " 7,75% = " +
                  "{0:.2f}".format(TaxCalculator.health_insurance_tax_secondary))
            print("Tax deductible expenses: ", TaxCalculator.t_deductibleExpenses)
            taxedIncome = d_income - TaxCalculator.t_deductibleExpenses
            taxedIncome0 = float("{0:.0f}".format(taxedIncome))
            print("Income: ", taxedIncome, " rounded: " + "{0:.0f}".format(taxedIncome0))
            TaxCalculator.calculateTax(taxedIncome0)
            print("Advance tax 18% = ", TaxCalculator.t_advance)
            print("Tax free income =", settings.REDUCED_TAX)
            taxPaid = TaxCalculator.t_advance - settings.REDUCED_TAX
            print("Reduced tax = " + "{0:.2f}".format(taxPaid))
            TaxCalculator.calculateAdvanceTax()
            TaxCalculator.advanceTax0 = float("{0:.0f}".format(TaxCalculator.advanceTax))
            print("Advance paid tax = " + "{0:.2f}".format(TaxCalculator.advanceTax) +
                  " rounded " + "{0:.0f}".format(TaxCalculator.advanceTax0))
            netIncome = TaxCalculator.income - ((TaxCalculator.t_socialSecurity + TaxCalculator.t_socialSecurityHealth
                                                 + TaxCalculator.t_socialSecuritySickness) + TaxCalculator.health_insurance_tax_rate_primary + TaxCalculator.advanceTax0)
            # store computed net income for external use/tests
            TaxCalculator.net_income = float("{0:.2f}".format(netIncome))
            print()
            print("Net income = " + "{0:.2f}".format(netIncome))

        elif TaxCalculator.contractType == "C":
            print("CIVIL")
            print("Income", TaxCalculator.income)
            d_income = TaxCalculator.calculateIncome(TaxCalculator.income)
            print("Social security tax: " + "{0:.2f}".format(TaxCalculator.t_socialSecurity))
            print("Health social security tax: " + "{0:.2f}".format(TaxCalculator.t_socialSecurityHealth))
            print("Sickness social security tax  " + "{0:.2f}".format(TaxCalculator.t_socialSecuritySickness))
            print("Income for calculating health security tax: ", d_income)
            TaxCalculator.calculateOtherTaxes(d_income)
            print("Health security tax: 9% = " \
                  + "{0:.2f}".format(TaxCalculator.health_insurance_tax_rate_primary) + " 7,75% = " +
                  "{0:.2f}".format(TaxCalculator.health_insurance_tax_secondary))
            settings.REDUCED_TAX = 0
            TaxCalculator.t_deductibleExpenses = d_income * settings.DEDUCTIBLE_EXPENSES["C"]
            print("Tax deductible expenses = ", TaxCalculator.t_deductibleExpenses)
            taxedIncome = d_income - TaxCalculator.t_deductibleExpenses
            taxedIncome0 = float("{0:.0f}".format(taxedIncome))
            print("income to be taxed: ", taxedIncome, " rounded: " + "{0:.0f}".format(taxedIncome0))
            TaxCalculator.calculateTax(taxedIncome0)
            print("Advance tax 18% =", TaxCalculator.t_advance)
            taxPaid = TaxCalculator.t_advance
            print("Already paid tax = " + "{0:.2f}".format(taxPaid))
            TaxCalculator.calculateAdvanceTax()
            TaxCalculator.advanceTax0 = float("{0:.0f}".format(TaxCalculator.advanceTax))
            print("Advance tax = " + "{0:.2f}".format(TaxCalculator.advanceTax) +
                  " rounded " + "{0:.0f}".format(TaxCalculator.advanceTax0))
            netIncome = TaxCalculator.income - ((TaxCalculator.t_socialSecurity + TaxCalculator.t_socialSecurityHealth
                                                 + TaxCalculator.t_socialSecuritySickness) + TaxCalculator.health_insurance_tax_rate_primary + TaxCalculator.advanceTax0)
            # store computed net income for external use/tests
            TaxCalculator.net_income = float("{0:.2f}".format(netIncome))
            print()
            print("Net income = " + "{0:.2f}".format(netIncome))
        else:
            print("Unknown type of contract!")

    @staticmethod
    def calculateAdvanceTax():
        TaxCalculator.advanceTax = TaxCalculator.t_advance - TaxCalculator.health_insurance_tax_secondary - settings.REDUCED_TAX

    @staticmethod
    def calculateTax(income):
        TaxCalculator.t_advance = income * settings.TAX_RATE

    @staticmethod
    def calculateIncome(income):
        TaxCalculator.t_socialSecurity = income * settings.SOCIAL_SECURITY_RATE
        TaxCalculator.t_socialSecurityHealth = income * settings.HEALTH_SECURITY_RATE
        TaxCalculator.t_socialSecuritySickness = income * settings.SICKNESS_SECURITY_RATE
        return (income - TaxCalculator.t_socialSecurity - TaxCalculator.t_socialSecurityHealth - TaxCalculator.t_socialSecuritySickness)

    @staticmethod
    def calculateOtherTaxes(income):
        TaxCalculator.health_insurance_tax_rate_primary = income * settings.HEALTH_INSURANCE_RATE_PRIMARY
        TaxCalculator.health_insurance_tax_secondary = income * settings.HEALTH_INSURANCE_RATE_FROM_TAX
