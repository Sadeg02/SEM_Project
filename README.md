# Tax Calculator

Tax calculator for calculating net income for Polish employment and civil contracts. The program automatically calculates all social security contributions, health insurance, deductible expenses, and taxes to show the actual amount you'll receive.

The program was refactored to be more readable and easier to extend with new features, taxes, or contract types. Tests were also added to verify its correctness.

## Project Structure

```
SEM_Refaktoryzacja/
├── src/tax_calculator/         # Main source code
│   ├── calculator.py           # Main TaxCalculator class
│   ├── settings.py             # Default settings (tax rates, etc.)
│   ├── tax_settings.py         # TaxSettings class for dependency injection
│   ├── main.py                 # Entry point
│   ├── strategies/             # Strategy pattern for different contract types
│   ├── presenters/             # Output formatting (presentation layer)
│   └── input_handlers/         # User input handling
├── tests/                      # Unit and integration tests
└── README.md                   # This file
```

---

## Refactoring History (commit by commit)

### 1. **Change static variable names**
**What I did:** Changed static variable names to more understandable ones.
**Why:** Code was unreadable with names like `t`, `ss`, `hs` - nobody knew what they meant.

### 2. **Add better initialization TaxCalculator class**
**What I did:** Improved TaxCalculator class initialization.
**Why:** Constructor was chaotic and needed organization.

### 3. **Add validation for initialization**
**What I did:** Added input validation (checking if income is a number, if contract type is valid).
**Why:** Without this, the program crashed on invalid data.

### 4. **Add simple unit tests**
**What I did:** Created first unit tests.
**Why:** To safely refactor - tests tell me if I broke something.

### 5. **Fix tests**
**What I did:** Fixed failing tests.
**Why:** Tests must pass, otherwise I don't know if code works.

### 6. **Refactor init function**
**What I did:** Extracted initialization logic to separate file `initialization.py`.
**Why:** TaxCalculator class was too big, needed to separate responsibilities (Single Responsibility Principle).

### 7. **Move static variables to settings file**
**What I did:** Moved all constants (social security rates, taxes) to separate `settings.py` file.
**Why:** To easily change configuration in one place instead of searching through entire code.

### 8. **Rename Class var/fun and convert to Instance Variable**
**What I did:** Changed class variables to instance variables + fixed names to snake_case.
- `income` → `gross_income`
- `contractType` → `contract_type`
- `t_socialSecurity` → `social_security_contribution`

**Why:**
- Class variables were shared between objects (bug!)
- Names didn't follow Python conventions (PEP 8)

### 9. **Separate printing logic and add tests**
**What I did:** Extracted printing logic to separate `TaxResultPrinter` class.
**Why:** Separation of business logic from presentation (Separation of Concerns). Also added tests for printer.

### 10. **Refactor of main logic of calculating**
**What I did:** Applied **Strategy Pattern** and **Factory Pattern**:
- Created `ContractStrategy` (base class)
- `EmploymentContractStrategy` and `CivilContractStrategy` (concrete strategies)
- `ContractStrategyFactory` to create appropriate strategy
- Split main `calculate()` method into small, single-purpose methods

**Why:**
- Removed code duplication (there were 2 similar methods for employment and civil contracts)
- Easy to add new contract type without changing existing code (Open/Closed Principle)
- Code is more readable - each method does one thing

### 11. **Instance isolation for settings**
**What I did:** Created `TaxSettings` class as dataclass and pass it to each calculator (Dependency Injection).
**Why:**
- Each calculator has its own settings (isolation)
- No global state (thread-safe)
- Easier testing - no need to reset global settings between tests

### 12. **Refactor printer to use dependency injection and fix naming bugs**
**What I did:**
- Fixed printer to use `calculator.settings` instead of global `settings`
- Added `PrintStrategyFactory`
- Fixed typos ("healt" → "health")
- Removed code duplication (printer uses calculator methods)

**Why:** Consistency with rest of project - Dependency Injection and Factory Pattern everywhere.

### 13. **Restructure project with clean architecture**
**What I did:**
- Renamed `sem_refaktoryzacja ` → `tax_calculator`
- Renamed `tax_calculator.py` → `calculator.py`
- Renamed `contracts/` → `strategies/` 
- Renamed `functions/` → `input_handlers/` (more precise naming)
- Added `__init__.py` to all packages (proper Python packages)


**Why:**
- Better naming reflects module purposes
- Proper Python packages (with __init__.py)

---

## Design Patterns

### 1. **Strategy Pattern**
**Where:** `strategies/contract_strategy.py`

**What it does:** Different strategies for calculating taxes for different contract types.
- `EmploymentContractStrategy` - for employment contracts
- `CivilContractStrategy` - for civil contracts

**Why:** Easy to add new contract type without changing existing code.

### 2. **Factory Pattern**
**Where:**
- `ContractStrategyFactory` in `strategies/contract_strategy.py`
- `PrintStrategyFactory` in `presenters/tax_result_printer.py`

**What it does:** Creates appropriate strategy object based on contract type.

**Why:** Centralizes object creation logic.

### 3. **Template Method Pattern**
**Where:** `calculator.py` - `calculate()` method

**What it does:** Defines algorithm skeleton (calculation order), delegates details to strategies.

**Why:** Ensures all calculations are done in correct order.

### 4. **Dependency Injection**
**Where:** `TaxSettings` passed to `TaxCalculator`

**What it does:** Calculator receives its settings from outside instead of using global ones.

**Why:** Each calculator can have different settings, easier testing.

---

## Tests

### Test Coverage
- **37 tests** total
- **3 test files**
- All tests passing (100% success rate)

### Test Types

**1. test_tax_calculator.py (5 tests)**
- Basic calculator functionality tests
- Invalid input validation
- Verify employment and civil contract results differ
- Edge cases (0 PLN, negative values)

**2. test_contract_strategy.py (17 tests)**
- Factory Pattern tests (creates correct strategy)
- Tests for each strategy separately
- Integration tests (employment and civil give different results)
- Tests that strategies use calculator settings

**3. test_tax_result_printer.py (15 tests)**
- Formatting tests (currency, rounding)
- Tests that printer displays all sections correctly
- PrintStrategyFactory tests
- Tests that employment and civil have different outputs
