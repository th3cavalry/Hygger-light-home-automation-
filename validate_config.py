#!/usr/bin/env python3
"""
Configuration Validator for Hygger Light Home Automation
Run this script to validate all YAML files for syntax errors.
"""

import yaml
import os
import sys

def validate_yaml_file(filepath):
    """Validate a single YAML file."""
    try:
        with open(filepath, 'r') as file:
            yaml.safe_load(file)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def main():
    """Main validation function."""
    print("🔍 Validating Hygger Light Home Automation Configuration...")
    print("=" * 60)
    
    errors = []
    success_count = 0
    total_count = 0
    
    # Find all YAML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                filepath = os.path.join(root, file)
                total_count += 1
                
                is_valid, error = validate_yaml_file(filepath)
                if is_valid:
                    print(f"✅ {filepath}")
                    success_count += 1
                else:
                    print(f"❌ {filepath}")
                    print(f"   Error: {error}")
                    errors.append((filepath, error))
    
    print("=" * 60)
    print(f"📊 Results: {success_count}/{total_count} files valid")
    
    if errors:
        print("\n🚨 Errors found:")
        for filepath, error in errors:
            print(f"  • {filepath}: {error}")
        sys.exit(1)
    else:
        print("🎉 All YAML files are valid!")
        
        # Additional checks
        print("\n🔧 Additional Recommendations:")
        print("  • Update entity IDs in scripts (remote.rm4_pro_remote)")
        print("  • Update weather entity ID (weather.openweathermap)")
        print("  • Ensure all helper entities are created in Home Assistant")
        print("  • Verify Broadlink and OpenWeatherMap integrations are working")

if __name__ == "__main__":
    main()