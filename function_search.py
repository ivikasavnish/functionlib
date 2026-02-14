#!/usr/bin/env python3
"""
Function Library Search Utility
Search functions WITHOUT vector store - direct text search
"""

import json
import re
from typing import List, Dict, Optional
from collections import defaultdict

class FunctionSearch:
    """Direct search without vector store"""
    
    def __init__(self, index_file='MASTER_INDEX.json'):
        """Load function index"""
        with open(index_file, 'r') as f:
            data = json.load(f)
        self.functions = data['functions']
        self.total = len(self.functions)
        
        # Build search indexes
        self._build_indexes()
        print(f"Loaded {self.total} functions")
    
    def _build_indexes(self):
        """Build inverted indexes for fast search"""
        self.name_index = defaultdict(list)
        self.category_index = defaultdict(list)
        self.purpose_index = defaultdict(list)
        self.word_index = defaultdict(list)
        
        for func in self.functions:
            # Index by name
            self.name_index[func['name']].append(func)
            
            # Index by category
            cat_key = f"{func['category']}/{func['subcategory']}"
            self.category_index[cat_key].append(func)
            
            # Index by words in purpose
            words = re.findall(r'\w+', func['purpose'].lower())
            for word in words:
                if len(word) > 2:  # Skip short words
                    self.word_index[word].append(func)
    
    def search_by_name(self, query: str, exact: bool = False) -> List[Dict]:
        """Search by function name"""
        query = query.lower()
        results = []
        
        for func in self.functions:
            name = func['name'].lower()
            if exact:
                if name == query:
                    results.append(func)
            else:
                if query in name:
                    results.append(func)
        
        return results
    
    def search_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Dict]:
        """Search by category"""
        if subcategory:
            key = f"{category}/{subcategory}"
            return self.category_index.get(key, [])
        else:
            results = []
            for func in self.functions:
                if func['category'] == category:
                    results.append(func)
            return results
    
    def search_by_purpose(self, query: str) -> List[Dict]:
        """Search in function purposes"""
        query = query.lower()
        results = []
        
        for func in self.functions:
            if query in func['purpose'].lower():
                results.append(func)
        
        return results
    
    def search_by_keywords(self, *keywords) -> List[Dict]:
        """Search by multiple keywords"""
        keyword_sets = []
        
        for keyword in keywords:
            keyword = keyword.lower()
            matching_funcs = set()
            
            # Search in name, purpose, category
            for func in self.functions:
                text = f"{func['name']} {func['purpose']} {func['category']} {func['subcategory']}"
                if keyword in text.lower():
                    matching_funcs.add(func['id'])
            
            keyword_sets.append(matching_funcs)
        
        # Intersection of all keyword sets (all keywords must match)
        if keyword_sets:
            matching_ids = set.intersection(*keyword_sets)
            results = [f for f in self.functions if f['id'] in matching_ids]
            return results
        
        return []
    
    def fuzzy_search(self, query: str, limit: int = 20) -> List[Dict]:
        """Fuzzy search across all fields"""
        query = query.lower()
        words = re.findall(r'\w+', query)
        
        # Score each function
        scored_results = []
        
        for func in self.functions:
            score = 0
            text = f"{func['name']} {func['purpose']} {func['category']} {func['subcategory']}".lower()
            
            # Exact name match - highest score
            if query in func['name'].lower():
                score += 100
            
            # Purpose match
            if query in func['purpose'].lower():
                score += 50
            
            # Word matches
            for word in words:
                if len(word) > 2:
                    if word in text:
                        score += 10
            
            # Category match
            if query in func['category'].lower():
                score += 20
            
            if score > 0:
                scored_results.append((score, func))
        
        # Sort by score
        scored_results.sort(reverse=True, key=lambda x: x[0])
        
        return [func for score, func in scored_results[:limit]]
    
    def search_similar_to(self, function_id: int, limit: int = 10) -> List[Dict]:
        """Find similar functions based on category and purpose"""
        target = next((f for f in self.functions if f['id'] == function_id), None)
        if not target:
            return []
        
        results = []
        
        # Same subcategory
        same_subcat = self.search_by_category(target['category'], target['subcategory'])
        results.extend([f for f in same_subcat if f['id'] != function_id])
        
        # If not enough, add from same category
        if len(results) < limit:
            same_cat = self.search_by_category(target['category'])
            for f in same_cat:
                if f['id'] != function_id and f not in results:
                    results.append(f)
                if len(results) >= limit:
                    break
        
        return results[:limit]
    
    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        """Autocomplete function names"""
        prefix = prefix.lower()
        matches = []
        
        for func in self.functions:
            if func['name'].lower().startswith(prefix):
                matches.append(func['name'])
            
            if len(matches) >= limit:
                break
        
        return matches
    
    def get_by_id(self, function_id: int) -> Optional[Dict]:
        """Get function by ID"""
        return next((f for f in self.functions if f['id'] == function_id), None)
    
    def list_categories(self) -> Dict[str, int]:
        """List all categories with counts"""
        categories = defaultdict(int)
        for func in self.functions:
            categories[func['category']] += 1
        return dict(categories)
    
    def list_subcategories(self, category: str) -> Dict[str, int]:
        """List subcategories for a category"""
        subcats = defaultdict(int)
        for func in self.functions:
            if func['category'] == category:
                subcats[func['subcategory']] += 1
        return dict(subcats)
    
    def random_functions(self, count: int = 5) -> List[Dict]:
        """Get random functions"""
        import random
        return random.sample(self.functions, min(count, len(self.functions)))
    
    def stats(self) -> Dict:
        """Get library statistics"""
        categories = self.list_categories()
        
        return {
            'total_functions': self.total,
            'categories': categories,
            'total_categories': len(categories)
        }


# CLI Interface
def main():
    """Command-line interface"""
    import sys
    
    search = FunctionSearch()
    
    print("\n" + "=" * 80)
    print("FUNCTION LIBRARY SEARCH")
    print("=" * 80)
    print(f"Total Functions: {search.total}")
    print()
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(f"Searching for: '{query}'")
        print("-" * 80)
        
        results = search.fuzzy_search(query, limit=20)
        
        if results:
            print(f"\nFound {len(results)} results:\n")
            for i, func in enumerate(results, 1):
                print(f"{i}. {func['name']}")
                print(f"   Category: {func['category']}/{func['subcategory']}")
                print(f"   Purpose: {func['purpose']}")
                print(f"   ID: {func['id']}")
                print()
        else:
            print("No results found.")
    else:
        # Interactive mode
        print("Enter search query (or 'help' for commands):")
        
        while True:
            try:
                query = input("\n> ").strip()
                
                if not query:
                    continue
                
                if query.lower() == 'exit':
                    break
                
                if query.lower() == 'help':
                    print("""
Commands:
  search <query>     - Search functions
  category <name>    - List functions in category
  stats              - Show statistics
  random             - Show random functions
  exit               - Exit
                    """)
                    continue
                
                if query.lower() == 'stats':
                    stats = search.stats()
                    print(f"\nTotal Functions: {stats['total_functions']}")
                    print("\nBy Category:")
                    for cat, count in stats['categories'].items():
                        print(f"  {cat}: {count}")
                    continue
                
                if query.lower() == 'random':
                    funcs = search.random_functions(5)
                    print("\nRandom Functions:")
                    for func in funcs:
                        print(f"  - {func['name']} ({func['category']})")
                    continue
                
                if query.lower().startswith('category '):
                    cat = query[9:].strip()
                    results = search.search_by_category(cat)
                    print(f"\nFunctions in '{cat}': {len(results)}")
                    for func in results[:10]:
                        print(f"  - {func['name']}")
                    if len(results) > 10:
                        print(f"  ... and {len(results) - 10} more")
                    continue
                
                # Default: fuzzy search
                results = search.fuzzy_search(query, limit=10)
                
                if results:
                    print(f"\nFound {len(results)} results:")
                    for i, func in enumerate(results, 1):
                        print(f"\n{i}. {func['name']}")
                        print(f"   {func['purpose']}")
                        print(f"   [{func['category']}/{func['subcategory']}]")
                else:
                    print("No results found.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break


if __name__ == '__main__':
    main()
