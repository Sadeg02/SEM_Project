# Tax settings configuration object for calculator instances
# Each TaxCalculator gets its own TaxSettings instance for isolation

from dataclasses import dataclass, field
from typing import Dict
import settings as global_settings


@dataclass
class TaxSettings:

    # Contract type constants
    contract_type_employment: str = field(default=global_settings.CONTRACT_TYPE_EMPLOYMENT)
    contract_type_civil: str = field(default=global_settings.CONTRACT_TYPE_CIVIL)

    # Social security rates
    social_security_rate: float = field(default=global_settings.SOCIAL_SECURITY_RATE)
    health_security_rate: float = field(default=global_settings.HEALTH_SECURITY_RATE)
    sickness_security_rate: float = field(default=global_settings.SICKNESS_SECURITY_RATE)

    # Health insurance rates
    health_insurance_rate_primary: float = field(default=global_settings.HEALTH_INSURANCE_RATE_PRIMARY)
    health_insurance_rate_from_tax: float = field(default=global_settings.HEALTH_INSURANCE_RATE_FROM_TAX)

    # Tax rates
    tax_rate: float = field(default=global_settings.TAX_RATE)

    # Tax-free amount by contract type
    reduced_tax: Dict[str, float] = field(default_factory=lambda: {
        global_settings.CONTRACT_TYPE_EMPLOYMENT: global_settings.REDUCED_TAX[global_settings.CONTRACT_TYPE_EMPLOYMENT],
        global_settings.CONTRACT_TYPE_CIVIL: global_settings.REDUCED_TAX[global_settings.CONTRACT_TYPE_CIVIL]
    })

    # Deductible expenses by contract type
    deductible_expenses: Dict[str, float] = field(default_factory=lambda: {
        global_settings.CONTRACT_TYPE_EMPLOYMENT: global_settings.DEDUCTIBLE_EXPENSES[global_settings.CONTRACT_TYPE_EMPLOYMENT],
        global_settings.CONTRACT_TYPE_CIVIL: global_settings.DEDUCTIBLE_EXPENSES[global_settings.CONTRACT_TYPE_CIVIL]
    })

    # Employment contract fixed deductible expense amount
    employment_fixed_deductible: float = field(default=global_settings.EMPLOYMENT_FIXED_DEDUCTIBLE)

    @classmethod
    def default(cls):
        # Create TaxSettings with default values from global settings module
        return cls()

    def copy(self, **changes):
        # Create a copy of settings with specified changes
        from dataclasses import replace
        return replace(self, **changes)
