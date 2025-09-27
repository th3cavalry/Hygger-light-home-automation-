# Troubleshooting Guide

This guide helps diagnose and fix common issues with the Hygger Light Home Automation system.

## Sync Lights Button Not Working

If the "Sync Lights" button doesn't affect the physical lights but manual `remote.send_command` works:

### Root Cause
This was typically caused by a weather forecast access error in the main automation. **This has been fixed in the latest version.**

### Verification Steps
1. Check if your automations are enabled:
   - Go to Settings > Automations & Scenes > Automations
   - Ensure `Aquarium Dynamic Circadian Lighting` is turned ON

2. Verify entity IDs match your setup:
   - Update `remote.rm4_pro_remote` to your actual Broadlink entity ID in all scripts
   - Update `weather.openweathermap` to your actual weather entity ID

3. Test the sync manually:
   - Go to Developer Tools > Services
   - Call `script.turn_on` with entity `script.sync_aquarium_lights`
   - Check Home Assistant logs for any errors

### Debug Process
1. **Check Helper Entities**: Ensure all helper entities exist:
   - `input_number.hygger_white_level`
   - `input_number.hygger_red_level`
   - `input_number.hygger_green_level`
   - `input_number.hygger_blue_level`
   - `input_boolean.enable_aquarium_lightning`
   - `input_text.aquarium_forecast_cache`

2. **Verify Weather Integration**: 
   - Go to Settings > Devices & Services
   - Check that OpenWeatherMap integration is working
   - Ensure API key is active (can take up to 2 hours after creation)

3. **Test IR Commands**:
   - Go to Developer Tools > Services
   - Test `remote.send_command` with your Broadlink entity
   - Use device: `hygger_hg016` and commands like `white_up`, `white_down`

## Other Common Issues

### Lights Not Responding at All
- Verify Broadlink RM4 Pro is connected to WiFi
- Check that all IR commands have been learned properly
- Test individual commands via Developer Tools

### Weather Data Not Updating
- Verify OpenWeatherMap API key is active
- Check that integration is configured for v3.0
- Look for errors in Home Assistant logs

### State Drift (Virtual vs Physical State)
- Use the "Sync Lights" button to reset everything
- Check that the daily reset automation is enabled
- Verify helper entities are updating correctly

## Getting Help

If issues persist:
1. Check Home Assistant logs for error messages
2. Verify all entity IDs match your actual entities
3. Ensure all required integrations are installed and working
4. Create an issue in the repository with:
   - Home Assistant version
   - Error messages from logs
   - Steps you've already tried