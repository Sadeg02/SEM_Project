from tax_calculator import TaxCalculator
from presenters.tax_result_printer import TaxResultPrinter

if __name__ == '__main__':
    # Create a printer for displaying results
    printer = TaxResultPrinter()

    # Tests with provided values
    print("=" * 50)
    print("Test 1: Employment Contract - 1000 PLN")
    print("=" * 50)
    calc_employment = TaxCalculator(
        income=1000,
        contract_type='E'
    )
    printer.print_results(calc_employment)

    print("\n" + "=" * 50)
    print("Test 2: Civil Contract - 1000 PLN")
    print("=" * 50)
    calc_civil = TaxCalculator(
        income=1000,
        contract_type='C'
    )
    printer.print_results(calc_civil)

    # Test with user input
    print("\n" + "=" * 50)
    print("Test 3: Interactive Input")
    print("=" * 50)
    calc_interactive = TaxCalculator()
    printer.print_results(calc_interactive)