import settings


class TaxResultPrinter:
    # Handles printing of tax calculation results using Template Method pattern

    def print_results(self, calculator):
        if calculator.contract_type == settings.CONTRACT_TYPE_EMPLOYMENT:
            strategy = EmploymentPrintStrategy()
        elif calculator.contract_type == settings.CONTRACT_TYPE_CIVIL:
            strategy = CivilPrintStrategy()
        else:
            print("Unknown type of contract!")
            return

        self._print_with_strategy(calculator, strategy)

    def _print_with_strategy(self, calc, strategy):
        # Template Method defining the printing algorithm skeleton
        self._print_section_header(strategy.get_contract_name())
        self._print_gross_income(calc)
        self._print_social_security_section(calc)
        self._print_health_insurance_section(calc)
        self._print_deductible_expenses_section(calc)
        self._print_taxable_income_section(calc)
        self._print_tax_calculation_section(calc, strategy)
        self._print_net_income(calc)

    def _print_section_header(self, contract_name):
        print(contract_name)

    def _print_gross_income(self, calc):
        print(f"Income {self._format_currency(calc.gross_income)}")

    def _print_social_security_section(self, calc):
        contributions = [
            ("Social security tax", calc.social_security_contribution),
            ("Health social security tax", calc.health_social_security_contribution),
            ("Sickness social security tax", calc.sickness_social_security_contribution)
        ]

        for label, amount in contributions:
            print(f"{label}: {self._format_currency(amount)}")

        income_after_social = self._calculate_income_after_social_security(calc)
        print(f"Income basis for healt social security: {self._format_currency(income_after_social)}")

    def _print_health_insurance_section(self, calc):
        print(f"Healt social security tax: 9% = {self._format_currency(calc.health_insurance_contribution)} "
              f"7,75% = {self._format_currency(calc.health_insurance_deductible)}")

    def _print_deductible_expenses_section(self, calc):
        print(f"Tax deductible expenses = {self._format_currency(calc.deductible_expenses)}")

    def _print_taxable_income_section(self, calc):
        income_after_social = self._calculate_income_after_social_security(calc)
        taxable_income = income_after_social - calc.deductible_expenses
        taxable_income_rounded = float("{0:.0f}".format(taxable_income))

        print(f"income to be taxed: {self._format_currency(taxable_income)} "
              f"rounded: {self._format_rounded(taxable_income_rounded)}")

    def _print_tax_calculation_section(self, calc, strategy):
        print(f"Advance tax 18% = {self._format_currency(calc.advance_tax_base)}")
        strategy.print_tax_details(calc, self)
        print(f"Advance paid tax = {self._format_currency(calc.advance_tax)} "
              f"rounded {self._format_rounded(calc.advance_tax_rounded)}")

    def _print_net_income(self, calc):
        print()
        print(f"Net income = {self._format_currency(calc.net_income)}")

    def _format_currency(self, amount):
        return "{0:.2f}".format(amount)

    def _format_rounded(self, amount):
        return "{0:.0f}".format(amount)

    def _calculate_income_after_social_security(self, calc):
        return (calc.gross_income -
                calc.social_security_contribution -
                calc.health_social_security_contribution -
                calc.sickness_social_security_contribution)


class PrintStrategy:
    # Base strategy for contract-specific printing variations

    def get_contract_name(self):
        raise NotImplementedError

    def print_tax_details(self, calc, printer):
        raise NotImplementedError


class EmploymentPrintStrategy(PrintStrategy):

    def get_contract_name(self):
        return "EMPLOYMENT"

    def print_tax_details(self, calc, printer):
        tax_free_amount = settings.REDUCED_TAX[settings.CONTRACT_TYPE_EMPLOYMENT]
        print(f"Tax free income = {printer._format_currency(tax_free_amount)}")
        reduced_tax = calc.advance_tax_base - tax_free_amount
        print(f"Reduced tax = {printer._format_currency(reduced_tax)}")


class CivilPrintStrategy(PrintStrategy):

    def get_contract_name(self):
        return "CIVIL"

    def print_tax_details(self, calc, printer):
        print(f"Already paid tax = {printer._format_currency(calc.advance_tax_base)}")
