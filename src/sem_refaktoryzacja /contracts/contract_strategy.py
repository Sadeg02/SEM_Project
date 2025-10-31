# Strategy pattern for handling contract-specific tax calculation rules

import settings


class ContractStrategyFactory:
    # Factory for creating the appropriate contract strategy

    @staticmethod
    def create_strategy(contract_type):
        # Create and return the appropriate strategy based on contract type
        if contract_type == settings.CONTRACT_TYPE_EMPLOYMENT:
            return EmploymentContractStrategy()
        elif contract_type == settings.CONTRACT_TYPE_CIVIL:
            return CivilContractStrategy()
        else:
            raise ValueError(f"Unknown contract type: {contract_type}")


class ContractStrategy:
    # Base strategy defining interface for contract-specific behavior

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
        return settings.CONTRACT_TYPE_EMPLOYMENT

    def calculate_deductible_expenses(self, income_after_social_security):
        # Employment contracts have fixed deductible expenses
        return settings.EMPLOYMENT_FIXED_DEDUCTIBLE

    def get_reduced_tax_amount(self):
        # Get employment-specific tax-free amount from settings
        return settings.REDUCED_TAX[settings.CONTRACT_TYPE_EMPLOYMENT]


class CivilContractStrategy(ContractStrategy):
    # Strategy for Civil (Umowa zlecenie) contract calculations

    def get_contract_type(self):
        return settings.CONTRACT_TYPE_CIVIL

    def calculate_deductible_expenses(self, income_after_social_security):
        # Civil contracts get 20% of income after social security as deductible
        return income_after_social_security * settings.DEDUCTIBLE_EXPENSES[settings.CONTRACT_TYPE_CIVIL]

    def get_reduced_tax_amount(self):
        # Get civil-specific tax-free amount from settings (which is 0)
        return settings.REDUCED_TAX[settings.CONTRACT_TYPE_CIVIL]
