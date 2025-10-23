class TaxCalculator(object):
    income = 0

    SOCIAL_SECURITY_RATE = 9.76 / 100
    HEALTH_SECURITY_RATE = 1.5 / 100
    SICKNESS_SECURITY_RATE = 2.45 / 100
    HEALTH_INSURANCE_RATE_PRIMARY = 9 / 100
    HEALTH_INSURANCE_RATE_FROM_TAX = 7.75 / 100
    TAX_RATE = 18 / 100
    REDUCED_TAX = 46.33

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
        if income is not None:
            TaxCalculator.income = float(income)
        else:
            while True:
                try:
                    TaxCalculator.income = float(input("Enter income: "))
                    break
                except ValueError:
                    print("Incorrect input. Please enter numeric value for income.")

        # Initialize contract type
        if contractType is not None:
            TaxCalculator.contractType = contractType.strip().upper()[0]
            # validate provided contract type early (non-interactive use)
            if TaxCalculator.contractType not in ("E", "C"):
                raise ValueError("Incorrect contract type. Use 'E' for Employment or 'C' for Civil.")
        else:
            while True:
                user_input = input("Enter contract type (E for Employment, C for Civil): ").strip().upper()
                if len(user_input) == 0:
                    print("Input cannot be empty. Please enter 'E' or 'C'.")
                    continue
                TaxCalculator.contractType = user_input[0]
                if TaxCalculator.contractType not in ("E", "C"):
                    print("Incorrect input. Please enter 'E' for Employment or 'C' for Civil.")
                else:
                    break


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
            print("Tax free income =", TaxCalculator.REDUCED_TAX)
            taxPaid = TaxCalculator.t_advance - TaxCalculator.REDUCED_TAX
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
            TaxCalculator.REDUCED_TAX = 0
            TaxCalculator.t_deductibleExpenses = (d_income * 20) / 100
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
        TaxCalculator.advanceTax = TaxCalculator.t_advance - TaxCalculator.health_insurance_tax_secondary - TaxCalculator.REDUCED_TAX

    @staticmethod
    def calculateTax(income):
        TaxCalculator.t_advance = (income * 18) / 100

    @staticmethod
    def calculateIncome(income):
        TaxCalculator.t_socialSecurity = (income * 9.76) / 100        
        TaxCalculator.t_socialSecurityHealth = (income * 1.5) / 100
        TaxCalculator.t_socialSecuritySickness = (income * 2.45) / 100
        return (income - TaxCalculator.t_socialSecurity - TaxCalculator.t_socialSecurityHealth - TaxCalculator.t_socialSecuritySickness)

    @staticmethod
    def calculateOtherTaxes(income):
        TaxCalculator.health_insurance_tax_rate_primary = (income * 9) / 100
        TaxCalculator.health_insurance_tax_secondary = (income * 7.75) / 100
