#!/usr/bin/env python3
"""
Test script to list all registered routes
"""

from app import create_app

def list_routes():
    app = create_app()
    
    print("All registered routes:")
    print("-" * 50)
    
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule:<40} {rule.endpoint:<30} {list(rule.methods)}")
    
    print("-" * 50)

if __name__ == '__main__':
    list_routes()
