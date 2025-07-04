#!/usr/bin/env python3
"""
Simple test script to verify the Flask application starts without errors.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    
    # Create the Flask app
    app = create_app()
    
    # Test that the app context works
    with app.app_context():
        print("✅ Flask application created successfully!")
        print(f"✅ App name: {app.name}")
        print(f"✅ Debug mode: {app.debug}")
        print(f"✅ Secret key configured: {'Yes' if app.secret_key else 'No'}")
        
        # Test route registration
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.rule} -> {rule.endpoint}")
        
        print(f"✅ Total routes registered: {len(routes)}")
        print("\n📋 Available routes:")
        for route in sorted(routes):
            print(f"  - {route}")
            
    print("\n🎉 All tests passed! The application is ready to run.")
    
except Exception as e:
    print(f"❌ Error creating Flask application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
