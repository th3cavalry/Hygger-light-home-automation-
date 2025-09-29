#!/usr/bin/env python3
"""
Hygger Light Diagnostic Tool
Helps diagnose why aquarium lights might not be turning on at expected times.
"""
import math
from datetime import datetime

def calculate_sun_elevation_fallback(hour):
    """Calculate sun elevation for zip code 47124 (Jeffersonville, Indiana: 38.28°N, 85.74°W)"""
    from datetime import datetime
    
    current_minute = datetime.now().minute
    day_of_year = datetime.now().timetuple().tm_yday
    
    if hour >= 6 and hour <= 18:
        # Seasonal adjustment: max sun elevation varies from ~28° (winter) to ~75° (summer)
        summer_peak = 75
        winter_peak = 28
        seasonal_range = summer_peak - winter_peak
        import math
        seasonal_offset = (day_of_year - 80) / 365 * 2 * math.pi
        seasonal_factor = winter_peak + seasonal_range * (1 + math.sin(seasonal_offset)) / 2
        
        # Calculate elevation based on time from solar noon
        hour_decimal = hour + (current_minute / 60.0)
        hours_from_noon = abs(hour_decimal - 12)
        if hours_from_noon <= 6:
            elevation_factor = 1 - (hours_from_noon / 6) ** 2
            return seasonal_factor * elevation_factor
        else:
            return 0
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
    
    # Calculate base brightness (updated to match outdoor light levels)
    current_hour = now.hour
    if current_hour >= 6 and current_hour <= 18:
        # Scale brightness to match natural outdoor illumination levels
        if sun_elevation > 60:
            base_brightness = 10  # High sun - maximum brightness
        elif sun_elevation > 40:
            base_brightness = int(8 + (sun_elevation - 40) / 10)  # Mid-day sun
        elif sun_elevation > 20:
            base_brightness = int(5 + (sun_elevation - 20) / 6.7)  # Morning/afternoon sun
        elif sun_elevation > 5:
            base_brightness = int(2 + (sun_elevation - 5) / 5)  # Low sun
        elif sun_elevation > 0:
            base_brightness = int(sun_elevation / 2.5)  # Twilight
        else:
            base_brightness = 0
        print(f"📊 Base brightness: {base_brightness} (calibrated for outdoor light levels)")
    else:
        base_brightness = 0
        print(f"📊 Base brightness: {base_brightness} (nighttime)")
    
    # Calculate each channel (updated for outdoor light matching)
    
    # White Channel - Primary illumination matching daylight
    if sun_elevation > 10:
        target_white = max(base_brightness, 1)
    elif sun_elevation > 0:
        target_white = int(base_brightness * 0.6)
    else:
        target_white = 0
    target_white = max(0, min(10, target_white))
    
    # Red Channel - Warm light for sunrise/sunset
    if sun_elevation < 20 and sun_elevation > 0:
        target_red = min(int(base_brightness * (1 - sun_elevation/20) * 1.5), 10)
    elif current_hour >= 8 and current_hour <= 16 and base_brightness > 2:
        target_red = int(max(base_brightness * 0.15, 1))
    else:
        target_red = 0
    target_red = max(0, min(10, target_red))
    
    # Green Channel - Natural balance
    if base_brightness > 1:
        target_green = int(target_white * 0.6 + target_red * 0.2 + base_brightness * 0.3)
    else:
        target_green = 0
    target_green = max(0, min(10, target_green))
    
    # Blue Channel - Peaks during high sun
    if sun_elevation > 20:
        target_blue = min(int(base_brightness * 0.8), 8)
    elif sun_elevation > 5:
        target_blue = min(int(base_brightness * 0.6), 6)
    elif current_hour >= 7 and current_hour <= 17 and base_brightness > 0:
        target_blue = int(max(base_brightness * 0.3, 1))
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