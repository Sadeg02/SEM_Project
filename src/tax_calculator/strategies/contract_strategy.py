# Strategy pattern for handling contract-specific tax calculation rules


class ContractStrategyFactory:
    # Factory for creating the appropriate contract strategy

    @staticmethod
    def create_strategy(contract_type, calculator):
        # Create and return the appropriate strategy based on contract type
        # Each strategy receives calculator reference to access its settings instance
        if contract_type == calculator.settings.contract_type_employment:
            return EmploymentContractStrategy(calculator)
        elif contract_type == calculator.settings.contract_type_civil:
            return CivilContractStrategy(calculator)
        else:
            raise ValueError(f"Unknown contract type: {contract_type}")


class ContractStrategy:
    # Base strategy defining interface for contract-specific behavior

    def __init__(self, calculator):
        # Each strategy stores reference to calculator to access its settings
        self.calculator = calculator

    def get_contract_type(self):
        # Return the contract type identifier
        raise NotImplementedError

    def calculate_deductible_expenses(self, income_after_social_security):
        # Calculate deductible expenses based on contract type
        raise NotImplementedError

    def get_reduced_tax_amount(self):
        # Get the tax-free amount for this contract type
        raise NotImplementedError


class EmploymentContractStrategy(ContractStrategy):
    # Strategy for Employment (Umowa o pracę) contract calculations

    def get_contract_type(self):
        return self.calculator.settings.contract_type_employment

    def calculate_deductible_expenses(self, income_after_social_security):
        # Employment contracts have fixed deductible expenses
        return self.calculator.settings.employment_fixed_deductible

    def get_reduced_tax_amount(self):
        # Get employment-specific tax-free amount from calculator's settings
        contract_type = self.calculator.settings.contract_type_employment
        return self.calculator.settings.reduced_tax[contract_type]


class CivilContractStrategy(ContractStrategy):
    # Strategy for Civil (Umowa zlecenie) contract calculations

    def get_contract_type(self):
        return self.calculator.settings.contract_type_civil

    def calculate_deductible_expenses(self, income_after_social_security):
        # Civil contracts get 20% of income after social security as deductible
        contract_type = self.calculator.settings.contract_type_civil
        deductible_rate = self.calculator.settings.deductible_expenses[contract_type]
        return income_after_social_security * deductible_rate

    def get_reduced_tax_amount(self):
        # Get civil-specific tax-free amount from calculator's settings (which is 0)
        contract_type = self.calculator.settings.contract_type_civil
        return self.calculator.settings.reduced_tax[contract_type]
