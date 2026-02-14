#!/usr/bin/env python3
"""
Search Examples - Quick Start
"""

from function_search import FunctionSearch

# Initialize search
search = FunctionSearch()

print("=" * 80)
print("FUNCTION SEARCH EXAMPLES")
print("=" * 80)

# Example 1: Search by name
print("\n1. Search by name (contains 'sort'):")
results = search.search_by_name('sort')
print(f"   Found {len(results)} functions")
for func in results[:5]:
    print(f"   - {func['name']}")

# Example 2: Search by category
print("\n2. Search by category (math/algebra):")
results = search.search_by_category('math', 'algebra')
print(f"   Found {len(results)} functions")
for func in results[:5]:
    print(f"   - {func['name']}")

# Example 3: Fuzzy search
print("\n3. Fuzzy search for 'calculate area':")
results = search.fuzzy_search('calculate area')
print(f"   Found {len(results)} functions")
for func in results[:5]:
    print(f"   - {func['name']}: {func['purpose']}")

# Example 4: Search by keywords
print("\n4. Search by keywords ('array', 'sort'):")
results = search.search_by_keywords('array', 'sort')
print(f"   Found {len(results)} functions")
for func in results[:5]:
    print(f"   - {func['name']}")

# Example 5: Find similar functions
print("\n5. Find similar to function ID 100:")
func = search.get_by_id(100)
if func:
    print(f"   Base function: {func['name']}")
    similar = search.search_similar_to(100, limit=5)
    print(f"   Similar functions:")
    for f in similar:
        print(f"   - {f['name']}")

# Example 6: Autocomplete
print("\n6. Autocomplete 'cal':")
suggestions = search.autocomplete('cal', limit=10)
for suggestion in suggestions:
    print(f"   - {suggestion}")

# Example 7: Statistics
print("\n7. Library statistics:")
stats = search.stats()
print(f"   Total functions: {stats['total_functions']}")
print(f"   Categories:")
for cat, count in stats['categories'].items():
    print(f"   - {cat}: {count}")

# Example 8: Random functions
print("\n8. Random functions:")
random_funcs = search.random_functions(5)
for func in random_funcs:
    print(f"   - {func['name']} ({func['category']})")

print("\n" + "=" * 80)
print("TRY IT YOURSELF:")
print("  python3 function_search.py <your query>")
print("  python3 function_search.py        (interactive mode)")
print("=" * 80)
