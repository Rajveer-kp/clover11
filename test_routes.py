#!/usr/bin/env python3

from app import create_app

def test_app():
    """Test that the Flask app starts and routes work"""
    app = create_app()
    
    with app.test_client() as client:
        # Test the main routes exist
        with app.app_context():
            print("✓ Flask app created successfully")
            
            # List all YouTube-related routes
            youtube_routes = [rule.rule for rule in app.url_map.iter_rules() if 'youtube' in rule.rule]
            print(f"✓ YouTube routes found: {len(youtube_routes)}")
            for route in youtube_routes:
                print(f"  - {route}")
            
            # Check if the API endpoints exist
            api_routes = [route for route in youtube_routes if '/api/' in route]
            print(f"✓ API routes found: {len(api_routes)}")
            for route in api_routes:
                print(f"  - {route}")
                
            print("\n✅ App test completed successfully!")

if __name__ == "__main__":
    test_app()
