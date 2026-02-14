# Function Index for LLM Processing

This index provides structured information about functions including name, purpose, inputs, and outputs.

## Total Functions: 48

---


## Category: math/algebra

### solve_linear_equation

**Purpose:** Solves linear equations of the form ax + b = 0

**Input:**
- `a`: number (coefficient)
- `b`: number (constant)

**Output:**
- `x`: number (solution)
- `steps`: array (solution steps)

---

### solve_quadratic_equation

**Purpose:** Solves quadratic equations using the quadratic formula

**Input:**
- `a`: number
- `b`: number
- `c`: number

**Output:**
- `roots`: array [x1, x2]
- `discriminant`: number

---

### solve_cubic_equation

**Purpose:** Solves cubic equations using Cardano's formula

**Input:**
- `a`: number
- `b`: number
- `c`: number
- `d`: number

**Output:**
- `roots`: array [x1, x2, x3]
- `type`: string

---

### factor_polynomial

**Purpose:** Factors polynomial expressions into simpler terms

**Input:**
- `coefficients`: array
- `degree`: integer

**Output:**
- `factors`: array
- `remainder`: number

---

### expand_polynomial

**Purpose:** Expands polynomial expressions

**Input:**
- `expression`: string

**Output:**
- `expanded`: string
- `coefficients`: array

---


## Category: math/calculus

### derivative

**Purpose:** Computes the derivative of a function

**Input:**
- `function`: string or callable
- `x`: number
- `method`: string

**Output:**
- `derivative`: number or function
- `formula`: string

---

### integral

**Purpose:** Computes indefinite or definite integral

**Input:**
- `function`: string or callable
- `variable`: string
- `limits`: optional array [a, b]

**Output:**
- `result`: number or expression
- `constant`: string

---

### limit

**Purpose:** Computes the limit of a function at a point

**Input:**
- `function`: string or callable
- `x`: number
- `approaching`: number or 'infinity'

**Output:**
- `limit`: number
- `exists`: boolean

---


## Category: math/geometry

### distance_2d

**Purpose:** Calculates distance between two points in 2D space

**Input:**
- `point1`: object {x, y}
- `point2`: object {x, y}

**Output:**
- `distance`: number

---

### triangle_area

**Purpose:** Calculates the area of a triangle

**Input:**
- `base`: number
- `height`: number
- `method`: string (base-height, heron, coordinates)

**Output:**
- `area`: number

---

### circle_area

**Purpose:** Calculates the area of a circle

**Input:**
- `radius`: number

**Output:**
- `area`: number
- `circumference`: number

---


## Category: math/trigonometry

### sin

**Purpose:** Calculates sine of an angle

**Input:**
- `angle`: number
- `unit`: string (radians or degrees)

**Output:**
- `result`: number (-1 to 1)

---

### cos

**Purpose:** Calculates cosine of an angle

**Input:**
- `angle`: number
- `unit`: string (radians or degrees)

**Output:**
- `result`: number (-1 to 1)

---


## Category: math/statistics

### mean

**Purpose:** Calculates arithmetic mean (average) of a dataset

**Input:**
- `data`: array of numbers

**Output:**
- `mean`: number
- `count`: integer

---

### median

**Purpose:** Calculates median (middle value) of a dataset

**Input:**
- `data`: array of numbers

**Output:**
- `median`: number

---

### standard_deviation

**Purpose:** Calculates standard deviation of a dataset

**Input:**
- `data`: array of numbers
- `sample`: boolean (default true)

**Output:**
- `stdDev`: number
- `variance`: number

---


## Category: math/probability

### combination

**Purpose:** Calculates number of combinations (n choose k)

**Input:**
- `n`: integer
- `k`: integer

**Output:**
- `result`: integer

---

### permutation

**Purpose:** Calculates number of permutations

**Input:**
- `n`: integer
- `k`: integer

**Output:**
- `result`: integer

---


## Category: science/physics

### calculate_force

**Purpose:** Calculates force using Newton's second law F=ma

**Input:**
- `mass`: number (kg)
- `acceleration`: number (m/s²)

**Output:**
- `force`: number (Newtons)
- `units`: string

---

### kinetic_energy

**Purpose:** Calculates kinetic energy KE = ½mv²

**Input:**
- `mass`: number (kg)
- `velocity`: number (m/s)

**Output:**
- `energy`: number (Joules)

---

### gravitational_force

**Purpose:** Calculates gravitational force between two masses

**Input:**
- `mass1`: number (kg)
- `mass2`: number (kg)
- `distance`: number (m)

**Output:**
- `force`: number (N)
- `acceleration`: number (m/s²)

---


## Category: science/chemistry

### molar_mass

**Purpose:** Calculates molar mass from molecular formula

**Input:**
- `formula`: string (e.g., H2O, CH4)

**Output:**
- `molarMass`: number (g/mol)
- `elements`: object

---

### ideal_gas_law

**Purpose:** Applies ideal gas law PV=nRT to solve for unknowns

**Input:**
- `P`: number (atm)
- `V`: number (L)
- `n`: number (mol)
- `T`: number (K)
- `solve_for`: string

**Output:**
- `result`: number
- `units`: string

---

### ph_calculation

**Purpose:** Calculates pH from hydrogen ion concentration

**Input:**
- `H_concentration`: number (mol/L)
- `pOH`: optional number

**Output:**
- `pH`: number (0-14)
- `pOH`: number
- `acidity`: string

---


## Category: science/electronics

### ohms_law

**Purpose:** Applies Ohm's law V=IR to solve for voltage, current, or resistance

**Input:**
- `V`: optional number (volts)
- `I`: optional number (amps)
- `R`: optional number (ohms)
- `solve_for`: string

**Output:**
- `result`: number
- `power`: number (watts)

---


## Category: coding/algorithms

### bubble_sort

**Purpose:** Sorts an array using bubble sort algorithm

**Input:**
- `array`: array of comparable items
- `ascending`: boolean (default true)

**Output:**
- `sorted`: array
- `comparisons`: integer
- `swaps`: integer

---

### quick_sort

**Purpose:** Sorts an array using quick sort algorithm

**Input:**
- `array`: array of comparable items
- `low`: integer
- `high`: integer

**Output:**
- `sorted`: array
- `complexity`: string

---

### binary_search

**Purpose:** Searches for element in sorted array using binary search

**Input:**
- `array`: sorted array
- `target`: any comparable type

**Output:**
- `index`: integer (-1 if not found)
- `iterations`: integer

---

### dijkstra_algorithm

**Purpose:** Finds shortest path in weighted graph using Dijkstra's algorithm

**Input:**
- `graph`: adjacency matrix or list
- `start`: node
- `end`: node

**Output:**
- `path`: array of nodes
- `distance`: number
- `visited`: array

---


## Category: coding/data_structures

### array_push

**Purpose:** Adds element to end of array

**Input:**
- `array`: array
- `element`: any type

**Output:**
- `array`: modified array
- `length`: integer

---

### binary_tree_insert

**Purpose:** Inserts node into binary tree

**Input:**
- `tree`: tree object
- `value`: comparable type

**Output:**
- `tree`: modified tree
- `inserted`: boolean

---

### hash_table_get

**Purpose:** Retrieves value from hash table by key

**Input:**
- `table`: hash table
- `key`: string or number

**Output:**
- `value`: any type or null
- `found`: boolean

---


## Category: coding/parsing

### parse_json

**Purpose:** Parses JSON string into object

**Input:**
- `json`: string
- `reviver`: optional function

**Output:**
- `data`: object
- `error`: null or error object

---


## Category: coding/validation

### validate_email

**Purpose:** Validates email address format

**Input:**
- `email`: string

**Output:**
- `valid`: boolean
- `message`: string

---


## Category: general_purpose/date_time

### parse_date

**Purpose:** Parses date string into date object

**Input:**
- `dateString`: string
- `format`: string (optional)

**Output:**
- `date`: Date object
- `valid`: boolean
- `timestamp`: number

---

### format_date

**Purpose:** Formats date object into string

**Input:**
- `date`: Date object
- `format`: string (YYYY-MM-DD, etc.)

**Output:**
- `formatted`: string

---

### add_days

**Purpose:** Adds specified number of days to a date

**Input:**
- `date`: Date object
- `days`: integer

**Output:**
- `newDate`: Date object
- `difference`: integer

---

### convert_timezone

**Purpose:** Converts date/time between timezones

**Input:**
- `date`: Date object
- `fromZone`: string
- `toZone`: string

**Output:**
- `convertedDate`: Date object
- `offset`: number

---


## Category: general_purpose/string_utilities

### trim

**Purpose:** Removes whitespace from both ends of string

**Input:**
- `str`: string

**Output:**
- `trimmed`: string
- `removed`: integer

---

### camel_case

**Purpose:** Converts string to camelCase format

**Input:**
- `str`: string

**Output:**
- `camelCase`: string

---

### truncate

**Purpose:** Truncates string to specified length

**Input:**
- `str`: string
- `length`: integer
- `ellipsis`: boolean (default true)

**Output:**
- `truncated`: string
- `wasTruncated`: boolean

---


## Category: general_purpose/validation

### validate_email

**Purpose:** Validates email address format

**Input:**
- `email`: string

**Output:**
- `valid`: boolean
- `message`: string
- `parts`: object {local, domain}

---


## Category: general_purpose/formatting

### format_currency

**Purpose:** Formats number as currency

**Input:**
- `amount`: number
- `currency`: string (USD, EUR, etc.)
- `locale`: string

**Output:**
- `formatted`: string
- `symbol`: string

---


## Category: general_purpose/conversion

### convert_units

**Purpose:** Converts between different units of measurement

**Input:**
- `value`: number
- `fromUnit`: string
- `toUnit`: string

**Output:**
- `converted`: number
- `factor`: number

---


## Category: general_purpose/random_generation

### generate_uuid

**Purpose:** Generates a UUID (Universally Unique Identifier)

**Input:**
- `version`: integer (1, 4, or 5)
- `namespace`: optional string

**Output:**
- `uuid`: string
- `version`: integer

---


## Category: general_purpose/hashing

### hash_md5

**Purpose:** Generates MD5 hash of input

**Input:**
- `data`: string or buffer
- `encoding`: string (hex, base64)

**Output:**
- `hash`: string
- `length`: integer

---


## Category: general_purpose/financial

### calculate_interest

**Purpose:** Calculates compound interest

**Input:**
- `principal`: number
- `rate`: number (percentage)
- `time`: number (years)
- `frequency`: integer

**Output:**
- `finalAmount`: number
- `interest`: number
- `breakdown`: array

---


## Category: general_purpose/geographic

### distance_between_coordinates

**Purpose:** Calculates distance between two geographic coordinates

**Input:**
- `lat1`: number
- `lon1`: number
- `lat2`: number
- `lon2`: number
- `unit`: string (km, miles)

**Output:**
- `distance`: number
- `bearing`: number

---

