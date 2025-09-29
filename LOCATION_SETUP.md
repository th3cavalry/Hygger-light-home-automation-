# Location-Specific Setup Guide

This system is now optimized for **zip code 47124 (Jeffersonville, Indiana)** and provides accurate solar positioning for reptile enclosure lighting.

## Location Details

- **Coordinates**: 38.28°N, 85.74°W
- **Timezone**: Eastern Time (America/New_York)
- **Solar Characteristics**:
  - Winter solstice noon: ~28° elevation
  - Summer solstice noon: ~75° elevation
  - Seasonal variation: 47° difference

## Lighting Improvements

### 🌅 Solar Position Accuracy
The system now uses location-specific calculations instead of generic assumptions:
- **Old system**: Assumed 90° peak sun elevation (unrealistic for latitude 38°N)
- **New system**: Accounts for actual 47-75° peak elevation range throughout the year

### 💡 Brightness Calibration  
Brightness levels now match natural outdoor illumination:
- **Twilight** (0-5° elevation): Very dim lighting (0-2/10)
- **Low sun** (5-20° elevation): Moderate brightness (2-5/10)
- **Mid sun** (20-40° elevation): Good brightness (5-8/10)
- **High sun** (40°+ elevation): Maximum brightness (8-10/10)

### 🌦️ Weather Integration
Weather adjustments preserve natural light ratios:
- **Cloudy**: 30-50% brightness reduction with enhanced warm tones
- **Rainy**: 60-70% brightness reduction with cooler color temperature
- **Partly Cloudy**: 15-20% brightness reduction

## Reptile Enclosure Optimization

### 📐 Enclosure Specifications
- **Size**: 4x2x2 feet
- **Construction**: Black PVC on 3 sides, glass front
- **Light**: Hygger HG016 24W LED with RGBW channels (0-10 levels each)

### 🎯 Uniform Light Distribution
The brightness calculations ensure uniform illumination throughout the enclosure:
- Accounts for light absorption by black PVC walls
- Optimized for front glass viewing area
- Prevents dark spots and uneven heating

### 🦎 Health Benefits
Location-accurate lighting provides:
- Natural circadian rhythm support
- Proper UVB simulation timing
- Temperature gradient alignment with natural patterns
- Behavioral cues matching wild habitat conditions

## Configuration Notes

### Home Assistant Sun Integration
The system will automatically use Home Assistant's sun integration when available, which provides:
- Real-time solar position data
- Automatic daylight saving time adjustment
- Precise sunrise/sunset timing

### Fallback Calculations
If the sun integration is unavailable, the system uses location-specific fallback calculations that account for:
- Seasonal sun elevation variations
- Time-based solar positioning
- Geographic latitude effects

## Customization for Other Locations

To adapt this system for different locations:

1. **Update coordinates** in the automation file:
   ```yaml
   # Change these values in aquarium_dynamic_circadian_lighting.yaml
   summer_peak = 75  # Your location's summer solstice noon elevation
   winter_peak = 28  # Your location's winter solstice noon elevation
   ```

2. **Calculate your location's solar elevations**:
   - Use online solar calculators for your coordinates
   - Measure peak elevation on summer solstice (June 21)
   - Measure peak elevation on winter solstice (December 21)

3. **Adjust for timezone**:
   - Ensure Home Assistant timezone matches your location
   - Update OpenWeatherMap integration for local weather

## Verification

To verify the location-specific improvements are working:

1. **Run diagnostic tool**:
   ```bash
   python3 diagnose_lighting.py
   ```

2. **Check solar elevation values**:
   - Should show realistic values for your location
   - Compare with online solar calculators for verification

3. **Monitor throughout seasons**:
   - Winter lighting should be dimmer and warmer
   - Summer lighting should be brighter with more blue
   - Seasonal transitions should be gradual and natural

## Troubleshooting Location Issues

### Sun Integration Not Working
If Home Assistant's sun integration is not providing data:
- Check that your location is set correctly in HA
- Verify timezone settings match your actual location
- The system will automatically use fallback calculations

### Lighting Too Bright/Dim
Adjust brightness scaling in the automation:
- Modify the brightness calculation factors
- Test different time periods to find optimal levels
- Consider enclosure-specific light absorption factors

### Weather Data Issues
Ensure OpenWeatherMap integration is working:
- Verify API key is active
- Check that weather entity provides condition data
- System will default to "sunny" if weather data unavailable