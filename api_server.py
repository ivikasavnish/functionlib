#!/usr/bin/env python3
"""
Function Library Search API
REST API for searching functions
"""

from flask import Flask, jsonify, request
from function_search import FunctionSearch

app = Flask(__name__)
search = FunctionSearch()

@app.route('/')
def home():
    """API home"""
    return jsonify({
        'name': 'Function Library Search API',
        'total_functions': search.total,
        'endpoints': {
            '/search': 'Search functions (query parameter)',
            '/function/<id>': 'Get function by ID',
            '/category/<name>': 'List functions in category',
            '/categories': 'List all categories',
            '/stats': 'Get statistics',
            '/random': 'Get random functions'
        }
    })

@app.route('/search')
def api_search():
    """Search endpoint"""
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    results = search.fuzzy_search(query, limit=limit)
    
    return jsonify({
        'query': query,
        'total_results': len(results),
        'results': results
    })

@app.route('/function/<int:func_id>')
def api_get_function(func_id):
    """Get function by ID"""
    func = search.get_by_id(func_id)
    
    if func:
        return jsonify(func)
    else:
        return jsonify({'error': 'Function not found'}), 404

@app.route('/category/<category>')
def api_category(category):
    """List functions in category"""
    subcategory = request.args.get('subcategory')
    results = search.search_by_category(category, subcategory)
    
    return jsonify({
        'category': category,
        'subcategory': subcategory,
        'total': len(results),
        'functions': results
    })

@app.route('/categories')
def api_categories():
    """List all categories"""
    return jsonify(search.list_categories())

@app.route('/stats')
def api_stats():
    """Get statistics"""
    return jsonify(search.stats())

@app.route('/random')
def api_random():
    """Get random functions"""
    count = int(request.args.get('count', 5))
    return jsonify(search.random_functions(count))

@app.route('/autocomplete')
def api_autocomplete():
    """Autocomplete function names"""
    prefix = request.args.get('prefix', '')
    limit = int(request.args.get('limit', 10))
    
    if not prefix:
        return jsonify({'error': 'Prefix parameter required'}), 400
    
    results = search.autocomplete(prefix, limit)
    
    return jsonify({
        'prefix': prefix,
        'suggestions': results
    })

if __name__ == '__main__':
    print("Starting Function Library Search API...")
    print(f"Loaded {search.total} functions")
    print("\nAvailable at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET /search?q=<query>")
    print("  GET /function/<id>")
    print("  GET /category/<category>")
    print("  GET /categories")
    print("  GET /stats")
    print("  GET /random")
    print("  GET /autocomplete?prefix=<prefix>")
    
    app.run(debug=True, port=5000)
