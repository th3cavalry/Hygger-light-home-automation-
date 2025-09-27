# Troubleshooting Guide

This guide helps diagnose and fix common issues with the Hygger Light Home Automation system.

## Sync Lights Button Not Working

### Problem 1: Nothing Happens When Clicking Sync Lights (Most Common)

If clicking the "Sync Lights" button does absolutely nothing - lights don't even reset to zero:

**Root Cause**: Entity IDs don't match your actual devices.

**Fix Steps**:
1. **Find your actual Broadlink entity ID**:
   - Go to Settings > Devices & Services
   - Find your Broadlink device
   - Note the entity ID (e.g., `remote.living_room_broadlink`)

2. **Update all scripts** with your actual entity ID:
   - Replace `remote.rm4_pro_remote` in all script files with your actual entity ID
   - Files to update: `scripts/aquarium_reset_to_zero.yaml`, `scripts/aquarium_reconcile_state.yaml`, `scripts/aquarium_lightning_effect.yaml`

3. **Test IR commands first**:
   - Go to Developer Tools > Services
   - Test `remote.send_command` with your actual entity ID
   - Use device: `hygger_hg016` and command: `white_down`
   - If this doesn't work, your IR commands aren't learned properly

### Problem 2: Lights Reset to Zero But Don't Adjust to Proper State

If lights reset to zero but don't adjust to proper brightness/color afterward:

**Root Cause**: Weather forecast access error in main automation (fixed in latest version).

**Verification Steps**:
1. Check if your automations are enabled:
   - Go to Settings > Automations & Scenes > Automations
   - Ensure `Aquarium Dynamic Circadian Lighting` is turned ON

2. Update weather entity ID:
   - Replace `weather.openweathermap` with your actual weather entity ID

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