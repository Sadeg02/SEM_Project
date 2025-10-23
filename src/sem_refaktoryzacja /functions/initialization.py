

def initialization_of_tax_calculator(TaxCalculator, income, contractType):
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