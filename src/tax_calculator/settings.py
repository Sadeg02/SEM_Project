# Tax Calculator Settings
# All rates are expressed as decimals (e.g., 0.10 = 10%)

# ========================================
# Contract Type Constants
# ========================================
CONTRACT_TYPE_EMPLOYMENT = "E"
CONTRACT_TYPE_CIVIL = "C"

# ========================================
# Social Security Rates
# ========================================
# Social security contributions (ZUS) - 9.76%
SOCIAL_SECURITY_RATE = 0.0976

# Health security contribution - 1.5%
HEALTH_SECURITY_RATE = 0.015

# Sickness security contribution - 2.45%
SICKNESS_SECURITY_RATE = 0.0245

# ========================================
# Health Insurance Rates
# ========================================
# Primary health insurance rate (full contribution) - 9%
HEALTH_INSURANCE_RATE_PRIMARY = 0.09

# Secondary health insurance rate (tax deductible portion) - 7.75%
HEALTH_INSURANCE_RATE_FROM_TAX = 0.0775

# ========================================
# Tax Rates
# ========================================
# Standard income tax rate - 18%
TAX_RATE = 0.18

# ========================================
# Tax-Free Amount by Contract Type
# ========================================
# Tax-free amount (kwota wolna od podatku)
# Employment: 46.33 PLN monthly
# Civil: 0 PLN (no tax-free amount)
REDUCED_TAX = {
    CONTRACT_TYPE_EMPLOYMENT: 46.33,  # Employment contract - has tax-free amount
    CONTRACT_TYPE_CIVIL: 0.0          # Civil contract - no tax-free amount
}

# ========================================
# Deductible Expenses by Contract Type
# ========================================
# Employment: 111.25 PLN fixed amount (calculated as multiplier of 1)
# Civil: 20% of income after social security contributions
DEDUCTIBLE_EXPENSES = {
    CONTRACT_TYPE_EMPLOYMENT: 1,     # Employment contract - fixed 111.25 PLN
    CONTRACT_TYPE_CIVIL: 0.2         # Civil contract - 20% of basis
}

# Employment contract fixed deductible expense amount
EMPLOYMENT_FIXED_DEDUCTIBLE = 111.25