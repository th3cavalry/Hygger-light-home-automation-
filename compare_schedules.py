#!/usr/bin/env python3
"""
Compare Old vs New Lighting Schedules
Shows the difference between fixed 6am-6pm schedule and dynamic sunrise/sunset.
"""
import math

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
        
        return f"{sunrise_hour:02d}:{sunrise_min:02d}", f"{sunset_hour:02d}:{sunset_min:02d}"
    except:
        # Fallback for extreme latitudes
        return "06:30", "18:30"

def main():
    """Compare old vs new lighting schedules."""
    print("⚖️  OLD vs NEW LIGHTING SCHEDULE COMPARISON")
    print("=" * 70)
    print()
    
    # Test key seasonal dates
    test_dates = [
        (21, "January 21 - Deep Winter"),
        (80, "March 21 - Spring Equinox"), 
        (172, "June 21 - Summer Solstice"),
        (266, "September 23 - Autumn Equinox"),
        (355, "December 21 - Winter Solstice")
    ]
    
    print("📅 Season               | 🕰️ Old Schedule | 🌅 New Schedule | 📊 Difference")
    print("-" * 70)
    
    for day_of_year, season in test_dates:
        sunrise, sunset = get_sunrise_sunset_for_day(day_of_year)
        
        # Old schedule: always 6:00 AM to 6:00 PM (12 hours)
        old_schedule = "06:00 - 18:00 (12.0h)"
        
        # New schedule: actual sunrise/sunset
        sr_parts = sunrise.split(':')
        ss_parts = sunset.split(':')
        sunrise_decimal = int(sr_parts[0]) + int(sr_parts[1]) / 60
        sunset_decimal = int(ss_parts[0]) + int(ss_parts[1]) / 60
        daylight_hours = sunset_decimal - sunrise_decimal
        
        new_schedule = f"{sunrise} - {sunset} ({daylight_hours:.1f}h)"
        
        # Calculate difference from 12 hour baseline
        diff_hours = daylight_hours - 12.0
        if diff_hours > 0:
            difference = f"+{diff_hours:.1f}h longer"
        elif diff_hours < 0:
            difference = f"{diff_hours:.1f}h shorter"
        else:
            difference = "Same length"
        
        print(f"{season:<22} | {old_schedule:<14} | {new_schedule:<14} | {difference}")
    
    print()
    print("🔍 KEY INSIGHTS:")
    print("• ❄️  OLD SYSTEM: Fixed 12-hour days year-round - not realistic!")
    print("• 🌍 NEW SYSTEM: Natural seasonal variation from 9.3h to 14.7h")
    print("• 🦎 Animals now experience authentic seasonal day length changes")
    print("• 🌿 Plants receive proper photoperiod signals for growth cycles")
    print("• 💤 Winter's shorter days encourage natural hibernation/dormancy")
    print("• 🌞 Summer's longer days support active growth and breeding")
    
    print()
    print("📈 BIOLOGICAL BENEFITS:")
    print("• Circadian rhythm regulation matches natural environment")
    print("• Seasonal behavioral cues (hibernation, reproduction, molting)")
    print("• Improved plant flowering and fruiting cycles")
    print("• Better vitamin D synthesis in reptiles/amphibians")
    print("• Reduced stress from artificial lighting schedules")

if __name__ == "__main__":
    main()