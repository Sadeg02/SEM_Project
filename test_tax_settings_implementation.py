#!/usr/bin/env python
"""
Simple script to verify TaxSettings implementation works correctly.
Each calculator should have its own isolated settings.
"""

import sys
import os

# Add src directory to path
ROOT = os.path.abspath(os.path.dirname(__file__))
MODULE_DIR = os.path.join(ROOT, 'src', 'sem_refaktoryzacja ')
if MODULE_DIR not in sys.path:
    sys.path.insert(0, MODULE_DIR)

from tax_calculator import TaxCalculator
from tax_settings import TaxSettings

print("=" * 60)
print("Testing TaxSettings Implementation")
print("=" * 60)

# Test 1: Default settings
print("\n1. Creating calculator with default settings...")
calc1 = TaxCalculator(income=1000, contract_type='E')
print(f"   Calculator 1 - Income: {calc1.gross_income}, Net: {calc1.net_income}")
print(f"   Settings reference: {id(calc1.settings)}")
assert calc1.net_income == 763.24, f"Expected 763.24, got {calc1.net_income}"
print("   ✓ Default settings work correctly")

# Test 2: Custom settings for one calculator
print("\n2. Creating calculator with custom settings...")
custom_settings = TaxSettings.default()
custom_settings.tax_rate = 0.20  # Change tax rate from 18% to 20%
calc2 = TaxCalculator(income=1000, contract_type='E', tax_settings=custom_settings)
print(f"   Calculator 2 - Income: {calc2.gross_income}, Net: {calc2.net_income}")
print(f"   Settings reference: {id(calc2.settings)}")
print(f"   Custom tax rate: {calc2.settings.tax_rate}")
print("   ✓ Custom settings work correctly")

# Test 3: Verify isolation - original calculator unchanged
print("\n3. Verifying settings isolation...")
calc3 = TaxCalculator(income=1000, contract_type='E')
print(f"   Calculator 3 - Income: {calc3.gross_income}, Net: {calc3.net_income}")
print(f"   Settings reference: {id(calc3.settings)}")
assert calc3.net_income == 763.24, f"Expected 763.24, got {calc3.net_income}"
assert calc1.settings.tax_rate == 0.18, "Original calculator settings should be unchanged"
assert calc2.settings.tax_rate == 0.20, "Custom calculator settings should remain custom"
assert calc3.settings.tax_rate == 0.18, "New calculator should have default settings"
print("   ✓ Settings are properly isolated between calculators")

# Test 4: Different contract types with same settings object
print("\n4. Testing different contract types...")
calc_employment = TaxCalculator(income=1000, contract_type='E')
calc_civil = TaxCalculator(income=1000, contract_type='C')
print(f"   Employment contract - Net: {calc_employment.net_income}")
print(f"   Civil contract - Net: {calc_civil.net_income}")
assert calc_employment.net_income == 763.24, "Employment calculation incorrect"
assert calc_civil.net_income == 728.24, "Civil calculation incorrect"
print("   ✓ Both contract types work correctly with isolated settings")

# Test 5: Strategy pattern uses calculator's settings
print("\n5. Verifying strategies use calculator's settings...")
assert calc_employment.contract_strategy.calculator.settings is calc_employment.settings
assert calc_civil.contract_strategy.calculator.settings is calc_civil.settings
print("   ✓ Strategies correctly reference calculator's settings")

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nKey benefits of TaxSettings implementation:")
print("• Each calculator has isolated settings (no global state)")
print("• Thread-safe - multiple calculators can run concurrently")
print("• Easy testing - no need to reset global settings")
print("• Flexible - each calculator can have different settings")
print("=" * 60)
