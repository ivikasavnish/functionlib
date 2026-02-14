# Example Function Files

This document shows examples of actual function documentation from the library.

## Math Example

### math/algebra/solve_quadratic_equation.md
```markdown
# solve_quadratic_equation

## Description
Solves quadratic equations using quadratic formula

## Category
math > algebra

## Usage
Common applications in mathematical computations and data analysis.

## Related Functions
See other functions in the algebra category.
```

---

## Science Example

### science/physics/kinetic_energy.md
```markdown
# kinetic_energy

## Description
Calculates kinetic energy KE=½mv²

## Category
science/physics

## Related Functions
See other functions in this category.
```

---

## Coding Example

### coding/algorithms/quick_sort.md
```markdown
# quick_sort

## Description
Sorts array using quick sort

## Category
coding/algorithms

## Related Functions
See other functions in this category.
```

---

## General Purpose Example

### general_purpose/date_time/parse_date.md
```markdown
# parse_date

## Description
Parses date from string

## Category
general_purpose/date_time

## Related Functions
See other functions in this category.
```

---

## Directory Listing Examples

### View all algebra functions:
```bash
ls math/algebra/
```

Output includes:
- solve_linear_equation.md
- solve_quadratic_equation.md
- solve_cubic_equation.md
- factor_polynomial.md
- expand_polynomial.md
- ... (350+ total)

### View all sorting algorithms:
```bash
ls coding/algorithms/ | grep sort
```

Output includes:
- bubble_sort.md
- quick_sort.md
- merge_sort.md
- heap_sort.md
- ... and more

### Count functions in a category:
```bash
ls math/calculus/ | wc -l
```

Output: ~350 functions

---

## Sample Function Content Structure

Every function file follows this template:

```markdown
# [function_name]

## Description
[What the function does - clear, concise description]

## Category
[category_path]

## Usage (optional)
[Common use cases and applications]

## Related Functions
[Links or references to similar functions]
```

---

## How Functions Are Organized

### By Domain
- **Math**: Mathematical operations and computations
- **Science**: Scientific formulas and calculations
- **Coding**: Programming algorithms and data structures
- **General Purpose**: Common utility functions

### By Specificity
Each category contains subcategories:
- math/ → algebra/ → solve_quadratic_equation.md
- science/ → physics/ → kinetic_energy.md
- coding/ → algorithms/ → quick_sort.md
- general_purpose/ → date_time/ → parse_date.md

### Naming Convention
- Descriptive names in lowercase
- Underscores separate words
- Extension: .md (Markdown)
- One function per file

---

## Search Examples

### Find all statistics functions:
```bash
find . -path "*/statistics/*" -name "*.md"
```

### Search for functions related to "matrix":
```bash
grep -r "matrix" --include="*.md" .
```

### List all physics formulas:
```bash
ls science/physics/ | head -20
```

---

## Function Count by Category

Total: **10,094 functions**

Breakdown:
- Math: 2,044 functions (20.2%)
- Science: 2,450 functions (24.3%)
- Coding: 2,800 functions (27.7%)
- General Purpose: 2,800 functions (27.7%)

This provides comprehensive coverage across all domains!
