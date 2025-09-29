#!/usr/bin/env python3
"""
Test Seasonal Lighting Variations
Demonstrates how the aquarium lighting will change throughout the year
following actual sunrise/sunset times instead of fixed 6am-6pm schedule.
"""
import math
from datetime import datetime, timedelta

def get_sunrise_sunset_for_day(day_of_year):
    """Get sunrise/sunset times for a specific day of year."""
    # Calculate sunrise/sunset for latitude 38.28°N (Jeffersonville, Indiana)
    latitude = 38.28
    
    # Solar declination angle
    declination = 23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 81)))
    
    # Hour angle at sunrise/sunset
    lat_rad = math.radians(latitude)
    decl_rad = math.radians(declination)
    
    try:
        hour_angle = math.degrees(math.acos(-math.tan(lat_rad) * math.tan(decl_rad)))
        
        # Convert to time (solar noon is around 12:00, adjust for time zone)
        sunrise_decimal = 12 - (hour_angle / 15) - 0.5  # Adjust for Eastern Time
        sunset_decimal = 12 + (hour_angle / 15) - 0.5
        
        # Convert to hours and minutes
        sunrise_hour = int(sunrise_decimal)
        sunrise_min = int((sunrise_decimal - sunrise_hour) * 60)
        sunset_hour = int(sunset_decimal)
        sunset_min = int((sunset_decimal - sunset_hour) * 60)
        
        # Calculate daylight length
        daylight_hours = sunset_decimal - sunrise_decimal
        
        return (f"{sunrise_hour:02d}:{sunrise_min:02d}", 
                f"{sunset_hour:02d}:{sunset_min:02d}", 
                daylight_hours)
    except:
        # Fallback for extreme latitudes
        return "06:30", "18:30", 12.0

def test_seasonal_variations():
    """Test lighting variations across different seasons."""
    print("🌱 SEASONAL AQUARIUM LIGHTING VARIATIONS")
    print("=" * 60)
    print("Now following actual sunrise/sunset times throughout the year!")
    print()
    
    # Test key dates throughout the year
    test_dates = [
        (1, "January 1 - Winter"),
        (60, "March 1 - Late Winter"),
        (80, "March 21 - Spring Equinox"),
        (121, "May 1 - Spring"),
        (172, "June 21 - Summer Solstice"),
        (213, "August 1 - Summer"),
        (266, "September 23 - Autumn Equinox"),
        (305, "November 1 - Autumn"),
        (355, "December 21 - Winter Solstice"),
        (365, "December 31 - Year End")
    ]
    
    print("📅 Date              | 🌅 Sunrise | 🌇 Sunset  | ⏱️ Daylight | 💡 Impact")
    print("-" * 80)
    
    for day_of_year, description in test_dates:
        sunrise, sunset, daylight_hours = get_sunrise_sunset_for_day(day_of_year)
        
        # Determine lighting impact
        if daylight_hours < 10:
            impact = "Short winter days - minimal lighting"
        elif daylight_hours < 12:
            impact = "Moderate lighting schedule"
        elif daylight_hours > 14:
            impact = "Long summer days - extended lighting"
        else:
            impact = "Balanced lighting schedule"
        
        print(f"{description:<18} | {sunrise:>7} | {sunset:>7} | {daylight_hours:>6.1f}h  | {impact}")
    
    print()
    print("✨ KEY BENEFITS:")
    print("• 🦎 Animals experience natural seasonal day length changes")
    print("• 🌿 Plants receive appropriate seasonal light cycles")
    print("• ❄️ Winter: Shorter days (9-10 hours) encourage hibernation/dormancy")
    print("• ☀️ Summer: Longer days (14-15 hours) support active growth")
    print("• 🔄 Gradual transitions help regulate biological rhythms")
    print("• 🌍 Realistic environmental simulation")

def test_daily_progression():
    """Test how lights change throughout a single day."""
    print("\n\n🕐 DAILY LIGHTING PROGRESSION EXAMPLE")
    print("=" * 60)
    print("Example: Summer day (June 21) with long daylight hours")
    
    # Use summer solstice (day 172)
    sunrise, sunset, daylight_hours = get_sunrise_sunset_for_day(172)
    print(f"Sunrise: {sunrise} | Sunset: {sunset} | Daylight: {daylight_hours:.1f} hours")
    print()
    
    # Parse sunrise/sunset times
    sr_parts = sunrise.split(':')
    ss_parts = sunset.split(':')
    sunrise_decimal = int(sr_parts[0]) + int(sr_parts[1]) / 60
    sunset_decimal = int(ss_parts[0]) + int(ss_parts[1]) / 60
    
    print("🕐 Time   | ☀️ Status      | 💡 Lighting Description")
    print("-" * 60)
    
    test_times = [
        (4, 0, "Pre-dawn"),
        (6, 0, "Sunrise"),
        (8, 0, "Morning"),
        (10, 0, "Mid-morning"),
        (12, 0, "Solar noon"),
        (14, 0, "Afternoon"),
        (16, 0, "Late afternoon"),
        (18, 0, "Evening"),
        (20, 0, "Sunset"),
        (22, 0, "Night")
    ]
    
    for hour, minute, period in test_times:
        time_decimal = hour + minute / 60
        
        if sunrise_decimal <= time_decimal <= sunset_decimal:
            status = "🌞 Daylight"
            if time_decimal < sunrise_decimal + 1:
                lighting = "🔴 Warm red/orange sunrise colors"
            elif time_decimal > sunset_decimal - 1:
                lighting = "🟠 Warm red/orange sunset colors"
            elif abs(time_decimal - 12) < 2:
                lighting = "⚪ Bright white/blue midday intensity"
            else:
                lighting = "🌈 Balanced full spectrum lighting"
        else:
            status = "🌙 Night"
            lighting = "⚫ Lights OFF - natural darkness"
        
        print(f"{hour:02d}:{minute:02d}    | {status:<12} | {lighting}")

def main():
    """Main test routine."""
    test_seasonal_variations()
    test_daily_progression()
    
    print("\n" + "=" * 60)
    print("🎉 CONCLUSION:")
    print("Your aquarium lights now follow realistic sunrise/sunset cycles!")
    print("This provides authentic seasonal variation for your plants and animals.")
    print("🔧 The system automatically adjusts daily - no manual intervention needed.")

if __name__ == "__main__":
    main()