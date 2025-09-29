#!/usr/bin/env python3
"""
Test script to verify the helper configurations are valid Home Assistant YAML.
This simulates what Home Assistant does when loading helper configurations.
"""

import yaml
import sys
import os

def test_helper_configs():
    """Test that helper configs only contain supported keys."""
    
    # Expected keys for each helper type based on Home Assistant documentation
    supported_keys = {
        'input_text': {'name', 'min', 'max', 'initial', 'unit_of_measurement'},
        'input_number': {'name', 'min', 'max', 'step', 'initial', 'unit_of_measurement'},
        'input_boolean': {'name', 'initial', 'icon'}  # icon IS supported for boolean
    }
    
    base_path = './helpers'
    
    test_files = [
        ('input_text.yaml', 'input_text'),
        ('input_numbers.yaml', 'input_number'),
        ('input_boolean.yaml', 'input_boolean')
    ]
    
    all_passed = True
    
    print("🧪 Testing Helper Configurations for Home Assistant Compatibility")
    print("=" * 70)
    
    for filename, config_type in test_files:
        filepath = os.path.join(base_path, filename)
        print(f"\n📁 Testing {filename}...")
        
        try:
            with open(filepath, 'r') as f:
                config = yaml.safe_load(f)
            
            if config_type not in config:
                print(f"❌ No {config_type} section found")
                all_passed = False
                continue
                
            helper_configs = config[config_type]
            
            for entity_id, entity_config in helper_configs.items():
                print(f"   🔍 Checking {entity_id}...")
                
                # Check for unsupported keys
                entity_keys = set(entity_config.keys())
                allowed_keys = supported_keys[config_type]
                unsupported_keys = entity_keys - allowed_keys
                
                if unsupported_keys:
                    print(f"   ❌ Unsupported keys found: {unsupported_keys}")
                    print(f"   ℹ️  Allowed keys for {config_type}: {allowed_keys}")
                    all_passed = False
                else:
                    print(f"   ✅ All keys are supported")
                    
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            all_passed = False
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All helper configurations are Home Assistant compatible!")
        print("✅ No unsupported keys found")
        print("✅ Configurations should import without 'extra keys not allowed' errors")
    else:
        print("❌ Some configurations have issues that need to be fixed")
        return False
        
    return True

if __name__ == "__main__":
    success = test_helper_configs()
    sys.exit(0 if success else 1)
