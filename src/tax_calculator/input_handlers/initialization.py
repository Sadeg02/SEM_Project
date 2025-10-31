def initialization_of_tax_calculator(calculator_instance, income, contract_type):
    if income is not None:
            calculator_instance.gross_income = float(income)
    else:
        while True:
            try:
                calculator_instance.gross_income = float(input("Enter income: "))
                break
            except ValueError:
                print("Incorrect input. Please enter numeric value for income.")

    # Initialize contract type
    if contract_type is not None:
        calculator_instance.contract_type = contract_type.strip().upper()[0]
        # validate provided contract type early (non-interactive use)
        valid_types = (calculator_instance.settings.contract_type_employment,
                      calculator_instance.settings.contract_type_civil)
        if calculator_instance.contract_type not in valid_types:
            raise ValueError("Incorrect contract type. Use 'E' for Employment or 'C' for Civil.")
    else:
        while True:
            user_input = input("Enter contract type (E for Employment, C for Civil): ").strip().upper()
            if len(user_input) == 0:
                print("Input cannot be empty. Please enter 'E' or 'C'.")
                continue
            calculator_instance.contract_type = user_input[0]
            valid_types = (calculator_instance.settings.contract_type_employment,
                          calculator_instance.settings.contract_type_civil)
            if calculator_instance.contract_type not in valid_types:
                print("Incorrect input. Please enter 'E' for Employment or 'C' for Civil.")
            else:
                break