# Dynamic Aquarium Lighting: A Home Assistant Project

This repository contains the complete configuration for a dynamic, weather-aware circadian lighting system for a Hygger HG016 aquarium light, controlled by Home Assistant. The system polls local weather forecasts and continuously adjusts the light's color and brightness to mimic the natural time of day and react to changing weather conditions, including thunderstorms.

## Features

* **Stateful Control**: The system tracks the virtual state of each color channel (R, G, B, W), allowing for precise, gradual transitions instead of abrupt scene changes.
* **Circadian Rhythm**: Automatically adjusts light color temperature and brightness based on actual sunrise and sunset times from your location, creating warm light at sunrise/sunset and cool, bright light at midday. Follows natural seasonal variations - short winter days (9-10 hours) and long summer days (14-15 hours).
* **Predictive Weather Mimicry**: Fetches the hourly weather forecast to proactively adjust the lighting for upcoming conditions like clouds, rain, and sun.
* **Dynamic Thunderstorm Effects**: When a thunderstorm is forecast, the system can trigger a special lightning effect. This feature can be easily enabled or disabled from the dashboard.
* **Robust Failsafes**:
  * Power Loss Recovery: Automatically re-syncs the light to the correct state upon Home Assistant startup.
  * Internet/API Outage Resilience: Caches a multi-day forecast locally, allowing the system to continue running with weather awareness even during an internet outage.
* **Full Manual Control**: A simple dashboard provides status information and manual controls to sync the lights or toggle special effects.

## System Architecture

The project is built around a central automation hub, Home Assistant, running in a virtual machine on a Proxmox server.

* **The Hub**: Home Assistant is the brain, responsible for all logic, scheduling, and state management.
* **Data Source**: The OpenWeatherMap API provides real-time and forecasted weather data.
* **Hardware Bridge**: A Broadlink RM4 Pro IR blaster receives commands from Home Assistant over the local network and transmits them to the Hygger light.
* **User Interface**: A simple, clean dashboard built within Home Assistant provides monitoring and control.

## Setup and Installation

### 1. Hardware Requirements

* A server running Proxmox VE.
* Hygger HG016 Aquarium Light with IR remote.
* Broadlink RM4 Pro Universal IR/RF Remote.

### 2. Software Installation

**Install Home Assistant OS on Proxmox:**
* Log into your Proxmox web UI, select your server node, and open the >_ Shell.
* Execute the following one-line command to run the community helper script. This will create a fully optimized VM for Home Assistant.
  ```bash
  bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
  ```
* Follow the prompts. It is recommended to use the "Advanced" settings to allocate at least 2 CPU cores and 4GB of RAM.
* Once complete, start the VM and navigate to its IP address on port 8123 (e.g., http://192.168.1.100:8123) to complete the Home Assistant onboarding.

**Integrate Hardware and Services:**

*Broadlink RM4 Pro:*
* Use the Broadlink mobile app to connect the RM4 Pro to your Wi-Fi. Stop the setup process in the app as soon as it is connected to your network to keep it unlocked for local control.
* Assign a static IP address to the RM4 Pro in your router's settings.
* In Home Assistant, go to Settings > Devices & Services and add the Broadlink integration, providing the static IP when prompted.

*OpenWeatherMap:*
* Create a free account at [OpenWeatherMap](https://openweathermap.org).
* Subscribe to the "One Call API 3.0" plan. You will need to enter payment info, but the free tier includes 1,000 calls/day.
* Copy your API key. Note that it may take up to 2 hours to become active.
* In Home Assistant, go to Settings > Devices & Services and add the OpenWeatherMap integration. Enter your API key and be sure to select mode v3.0.

### 3. Capture IR Commands

Using the Home Assistant interface, you need to teach the Broadlink the individual commands for adjusting each color's brightness.

* Go to Developer Tools > Actions.
* Search for and select `Remote: Learn command`.
* Choose your Broadlink device as the target.
* Use the following device and command names to learn each of the eight required buttons one by one. After entering the names, click "Perform action" and press the corresponding button on the Hygger remote.
  * `white_up`, `white_down`
  * `red_up`, `red_down`
  * `green_up`, `green_down`
  * `blue_up`, `blue_down`
  * `weather_lightning` (for the thunderstorm effect)

## Home Assistant Configuration

All the following code should be added to your Home Assistant configuration. You can do this through the UI editors or by editing your YAML files directly (e.g., automations.yaml, scripts.yaml).

### 1. Helper Entities

These helpers are the system's "memory." Create them in Settings > Devices & Services > Helpers.

**Number Helpers (x4)**: Create four "Number" helpers to track the state of each color channel.
* Name: Hygger White Level, Hygger Red Level, etc.
* Min: 0, Max: 10, Step: 1
* Mode: Slider

**Toggle Helper (x1)**: Create one "Toggle" helper to enable/disable the lightning effect.
* Name: Enable Aquarium Lightning

**Text Helper (x1)**: Create one "Text" helper to cache the weather forecast.
* Name: Aquarium Forecast Cache

### 2. Scripts

Create the following scripts under Settings > Automations & Scenes > Scripts.

See the `scripts/` directory for complete YAML configurations:
- `script.aquarium_reconcile_state`
- `script.aquarium_lightning_effect`
- `script.aquarium_reset_to_zero`
- `script.sync_aquarium_lights`
- `script.aquarium_test_lights` - Sequential test script for troubleshooting

### 3. Automations

Create the following automations under Settings > Automations & Scenes > Automations.

See the `automations/` directory for complete YAML configurations:
- `automation.aquarium_dynamic_circadian_lighting`
- `automation.aquarium_daily_reset`
- `automation.aquarium_startup_sync`
- `automation.aquarium_forecast_caching`

## Dashboard Configuration

Create a new dashboard for this project for a clean interface.

* Go to Settings > Dashboards and create a new dashboard called "Aquarium Control".
* Open the new dashboard and enter Edit Dashboard mode.
* Add Weather Card: Add a Weather Forecast card and link it to your `weather.openweathermap` entity to see the current data source.
* Add Control Card: Add an Entities card and include the following helpers:
  * `input_boolean.enable_aquarium_lightning` (Your lightning toggle)
  * `script.sync_aquarium_lights` (Your manual sync button)
  * The four `input_number` helpers (e.g., `input_number.hygger_white_level`) to monitor the current virtual state.

## Final Deployment Step

⚠️ **IMPORTANT**: Before testing, you must update the entity IDs in all configuration files to match your actual Home Assistant entities:

1. **Update Broadlink Entity ID**: Replace `remote.rm4_pro_remote` with your actual Broadlink entity ID in ALL script files
2. **Update Weather Entity ID**: Replace `weather.openweathermap` with your actual weather entity ID in automation files
3. **Ensure all helper entities are created** as described in the Home Assistant Configuration section

Once all the helpers, scripts, and automations are created and enabled, and entity IDs are updated, your final step is to perform the initial synchronization.

**Press the "Sync Lights" button on your dashboard.**

This will force the light to a known zero state and then immediately ramp it up to the correct color and brightness for the current time of day and weather. Your system is now fully operational.

**If nothing happens when you click "Sync Lights", see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - this is usually caused by incorrect entity IDs.**

## Files in this Repository

- `README.md` - This documentation
- `SETUP_GUIDE.md` - Step-by-step setup instructions
- `TROUBLESHOOTING.md` - Troubleshooting guide for common issues
- `validate_config.py` - Configuration validation script
- `check_entities.py` - Entity ID configuration checker
- `test_lights.py` - Python script to simulate the light test sequence
- `scripts/` - Home Assistant script configurations
- `automations/` - Home Assistant automation configurations
- `dashboard/` - Dashboard YAML configuration
- `helpers/` - Helper entity configurations

## Testing Your Setup

### Light Test Script

The system includes a comprehensive test script that cycles through each color channel to verify proper operation:

**Home Assistant Script**: `script.aquarium_test_lights`
- Sequence: White (0→10→0) → Red (0→10→0) → Green (0→10→0) → Blue (0→10→0) → All Zero
- Import this script into Home Assistant and run it to test all IR commands
- Ideal for initial setup verification and troubleshooting

**Python Simulation**: `python3 test_lights.py`
- Runs a visual simulation of the test sequence in your terminal
- Useful for understanding the test pattern without hardware
- No Home Assistant required

### Diagnostic Tools

**Lighting Diagnostic Tool**: `python3 diagnose_lighting.py`
- Diagnoses why lights might not be turning on at expected times
- Shows expected light levels for current time
- Checks common configuration issues
- Provides step-by-step troubleshooting guidance

### Configuration Validation

Run the included validation script to check your configuration:
```bash
python3 validate_config.py
```

Run the entity checker to identify configuration issues:
```bash
python3 check_entities.py
```

## Troubleshooting

### Common Issues

1. **Sync Lights button does nothing at all**: Most commonly caused by incorrect entity IDs. Update `remote.rm4_pro_remote` and `weather.openweathermap` to match your actual entities. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
2. **Lights not responding**: Check that your Broadlink RM4 Pro is connected and that all IR commands have been properly learned.
3. **Weather data not updating**: Verify your OpenWeatherMap API key is active and the integration is configured for v3.0.
4. **State drift**: Run the sync script manually or wait for the daily reset at 2:00 AM.

### Manual Reset

If the system gets out of sync, you can always use the "Sync Lights" button on the dashboard to reset everything to the correct state.

## Contributing

Feel free to submit issues or pull requests to improve this aquarium lighting automation system.