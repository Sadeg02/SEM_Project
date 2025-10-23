from tax_calculator import TaxCalculator

if __name__=='__main__':
    # Tests with provided values
    TaxCalculator(
        income=1000,
        contractType='E'
    )
    TaxCalculator(
        income=1000,
        contractType='C'
    )
    # Test with user input
    TaxCalculator()