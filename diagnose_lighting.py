#!/usr/bin/env python3
"""
Hygger Light Diagnostic Tool
Helps diagnose why aquarium lights might not be turning on at expected times.
"""
import math
from datetime import datetime

def calculate_sun_elevation_fallback(hour):
    """Calculate approximate sun elevation based on time of day."""
    if hour >= 6 and hour <= 18:
        if hour <= 12:
            return (hour - 6) * 15
        else:
            return 90 - ((hour - 12) * 15)
    else:
        return 0

def diagnose_current_time():
    """Diagnose lighting calculations for the current time."""
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    
    print(f"🕰️  Current time: {current_hour:02d}:{current_minute:02d}")
    print("=" * 50)
    
    # Calculate expected sun elevation
    sun_elevation = calculate_sun_elevation_fallback(current_hour)
    print(f"🌅 Expected sun elevation: {sun_elevation}°")
    
    # Calculate base brightness
    calculated_base = max(0, min(10, round(sun_elevation / 9)))
    if current_hour >= 7 and current_hour <= 19:
        base_brightness = max(2, calculated_base)
        print(f"📊 Base brightness: {base_brightness} (with daytime minimum of 2)")
    else:
        base_brightness = calculated_base
        print(f"📊 Base brightness: {base_brightness} (no daytime minimum)")
    
    # Calculate each channel
    # White Channel
    if sun_elevation > 10:
        target_white = min(round(base_brightness * (sun_elevation / 90) * 1.2), 10)
    elif current_hour >= 7 and current_hour <= 19:
        target_white = max(base_brightness, 2)
    else:
        target_white = round(base_brightness * 0.5)
    target_white = max(0, min(10, target_white))
    
    # Red Channel
    if sun_elevation < 15:
        target_red = min(round(base_brightness * (1 - (sun_elevation/15)) * 1.5), 10)
    else:
        target_red = 0
    target_red = max(0, min(10, target_red))
    
    # Green Channel
    target_green = round(target_white * 0.5 + target_red * 0.5)
    target_green = max(0, min(10, target_green))
    
    # Blue Channel
    if sun_elevation > 5:
        target_blue = min(round(base_brightness * (sun_elevation / 90) * 0.8), 8)
    elif current_hour >= 8 and current_hour <= 18:
        target_blue = max(round(base_brightness * 0.4), 1)
    else:
        target_blue = 0
    target_blue = max(0, min(10, target_blue))
    
    print(f"🎯 Expected light levels:")
    print(f"   ⚪ White: {target_white}/10")
    print(f"   🔴 Red: {target_red}/10")
    print(f"   🟢 Green: {target_green}/10") 
    print(f"   🔵 Blue: {target_blue}/10")
    
    total_brightness = target_white + target_red + target_green + target_blue
    print(f"💡 Total expected brightness: {total_brightness}/40")
    
    if total_brightness == 0:
        print("❌ DIAGNOSIS: Lights should be OFF at this time")
        if current_hour >= 6 and current_hour <= 20:
            print("⚠️  WARNING: This seems unusual for daytime hours!")
    else:
        print("✅ DIAGNOSIS: Lights should be ON at this time")
    
    return total_brightness > 0

def check_common_issues():
    """Check for common configuration issues."""
    print("\n🔍 Common Issues Checklist:")
    print("=" * 50)
    
    issues_found = []
    
    print("1. ⚙️  Helper Entities")
    print("   Required entities in Home Assistant:")
    required_helpers = [
        'input_number.hygger_white_level',
        'input_number.hygger_red_level',
        'input_number.hygger_green_level', 
        'input_number.hygger_blue_level',
        'input_boolean.enable_aquarium_lightning',
        'input_text.aquarium_forecast_cache'
    ]
    for helper in required_helpers:
        print(f"   ➤ {helper}")
    
    print("\n2. 🔌 Entity ID Configuration")
    print("   Check these entity IDs match your actual devices:")
    print("   ➤ remote.rm4_pro_remote (Broadlink device)")
    print("   ➤ weather.openweathermap (Weather integration)")
    
    print("\n3. 🤖 Automation Status")
    print("   Verify in Home Assistant:")
    print("   ➤ 'Aquarium Dynamic Circadian Lighting' automation is ENABLED")
    print("   ➤ Automation is not stuck in an error state")
    print("   ➤ Check Home Assistant logs for errors")
    
    print("\n4. 📡 Hardware Connectivity")
    print("   ➤ Broadlink RM4 Pro is connected to WiFi")
    print("   ➤ IR commands have been learned properly")
    print("   ➤ Test IR commands manually via Developer Tools")
    
    print("\n5. 🌐 Weather Integration")
    print("   ➤ OpenWeatherMap integration is working")
    print("   ➤ API key is valid and active")
    print("   ➤ Weather entity provides current conditions")

def main():
    """Main diagnostic routine."""
    print("🔧 Hygger Aquarium Light Diagnostic Tool")
    print("=" * 50)
    print("This tool helps diagnose why your lights might not be working.")
    print()
    
    # Diagnose current time
    lights_should_be_on = diagnose_current_time()
    
    # Check common issues
    check_common_issues()
    
    print("\n" + "=" * 50)
    print("💡 Quick Fix Steps:")
    if lights_should_be_on:
        print("1. Try the 'Sync Lights' button in your aquarium dashboard")
        print("2. Check that the automation is enabled and running")
        print("3. Verify entity IDs match your actual devices")
        print("4. Test IR commands manually in Developer Tools")
    else:
        print("1. Lights appear to be correctly OFF for this time")
        print("2. If you expect them to be ON, check the time calculations")
        print("3. Consider adjusting the lighting schedule parameters")
    
    print("\n📚 For detailed troubleshooting, see TROUBLESHOOTING.md")
    print("🆘 For help, create an issue at: https://github.com/th3cavalry/Hygger-light-home-automation-")

if __name__ == "__main__":
    main()