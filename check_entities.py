#!/usr/bin/env python3
"""
Entity Checker for Hygger Light Home Automation
This script helps identify common entity ID configuration issues.
"""

import yaml
import os
import re

def check_entity_ids():
    """Check for default entity IDs that need to be updated."""
    print("🔍 Checking for entity IDs that need to be updated...")
    print("=" * 60)
    
    default_entities = {
        'remote.rm4_pro_remote': 'Broadlink remote entity (MUST be updated)',
        'weather.openweathermap': 'Weather entity (MUST be updated to match your integration)'
    }
    
    issues = []
    
    # Find all YAML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    for entity_id, description in default_entities.items():
                        if entity_id in content:
                            issues.append({
                                'file': filepath,
                                'entity_id': entity_id,
                                'description': description
                            })
                            
                except Exception as e:
                    print(f"⚠️  Could not read {filepath}: {e}")
    
    if issues:
        print("❌ Found default entity IDs that need to be updated:")
        print()
        
        current_file = None
        for issue in issues:
            if issue['file'] != current_file:
                print(f"📁 {issue['file']}:")
                current_file = issue['file']
            print(f"   • {issue['entity_id']} - {issue['description']}")
        
        print("\n🔧 To fix these issues:")
        print("1. Find your actual entity IDs in Home Assistant:")
        print("   - Settings > Devices & Services")
        print("   - Look for your Broadlink and Weather integrations")
        print("2. Replace the default entity IDs with your actual ones")
        print("3. Run this script again to verify")
        
    else:
        print("✅ No default entity IDs found - configuration looks good!")
    
    print("\n" + "=" * 60)
    
    # Check for required helper entities
    print("📋 Required helper entities (create these in Home Assistant):")
    required_helpers = [
        'input_number.hygger_white_level',
        'input_number.hygger_red_level', 
        'input_number.hygger_green_level',
        'input_number.hygger_blue_level',
        'input_boolean.enable_aquarium_lightning',
        'input_text.aquarium_forecast_cache'
    ]
    
    for helper in required_helpers:
        print(f"   • {helper}")
    
    print("\nCreate these in: Settings > Devices & Services > Helpers")

if __name__ == "__main__":
    check_entity_ids()