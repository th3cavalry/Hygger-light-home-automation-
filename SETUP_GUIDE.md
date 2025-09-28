# Step-by-Step Setup Guide

This guide walks you through setting up the Dynamic Aquarium Lighting system from start to finish.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Proxmox server running
- [ ] Hygger HG016 Aquarium Light with IR remote
- [ ] Broadlink RM4 Pro Universal IR/RF Remote
- [ ] OpenWeatherMap account with API key
- [ ] Static IP address for your Broadlink device

## Step 1: Install Home Assistant

1. **Create Home Assistant VM on Proxmox:**
   ```bash
   bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
   ```

2. **VM Configuration:**
   - Use "Advanced" settings
   - Allocate at least 2 CPU cores
   - Allocate at least 4GB RAM
   - Start the VM after creation

3. **Complete Onboarding:**
   - Navigate to `http://[VM-IP]:8123`
   - Follow the setup wizard
   - Create your admin account

## Step 2: Hardware Integration

### Configure Broadlink RM4 Pro

1. **Connect to WiFi:**
   - Use the Broadlink mobile app
   - Connect the RM4 Pro to your network
   - **Important:** Stop setup in the app after WiFi connection to keep it unlocked

2. **Set Static IP:**
   - In your router settings, assign a static IP to the RM4 Pro
   - Note this IP address for Home Assistant configuration

3. **Add to Home Assistant:**
   - Go to Settings > Devices & Services
   - Click "Add Integration"
   - Search for "Broadlink"
   - Enter the static IP address

### Configure OpenWeatherMap

1. **Create Account:**
   - Go to [openweathermap.org](https://openweathermap.org)
   - Create a free account

2. **Subscribe to API:**
   - Subscribe to "One Call API 3.0" (free tier: 1,000 calls/day)
   - Enter payment information (required but free tier won't charge)
   - Copy your API key

3. **Add to Home Assistant:**
   - Go to Settings > Devices & Services
   - Click "Add Integration"
   - Search for "OpenWeatherMap"
   - Enter API key and select mode v3.0
   - **Note:** API key may take up to 2 hours to become active

## Step 3: Learn IR Commands

You need to teach the Broadlink the IR commands from your Hygger remote.

1. **Open Developer Tools:**
   - Go to Developer Tools > Actions
   - Search for and select: `Remote: Learn command`
   - Choose your Broadlink device as target

2. **Learn Each Command:**
   Learn these commands one by one:
   - Device: `hygger_hg016`
   - Commands to learn:
     - `white_up`
     - `white_down`
     - `red_up`
     - `red_down`
     - `green_up`
     - `green_down`
     - `blue_up`
     - `blue_down`
     - `weather_lightning` (for thunderstorm effect)

3. **Learning Process:**
   - Enter device name: `hygger_hg016`
   - Enter command name (e.g., `white_up`)
   - Click "Perform action"
   - Press the corresponding button on your Hygger remote
   - Repeat for all 9 commands

## Step 4: Create Helper Entities

Create these helpers in Settings > Devices & Services > Helpers:

### Number Helpers (Create 4)
- **Name:** Hygger White Level
  - Min: 0, Max: 10, Step: 1, Mode: Slider
- **Name:** Hygger Red Level
  - Min: 0, Max: 10, Step: 1, Mode: Slider
- **Name:** Hygger Green Level
  - Min: 0, Max: 10, Step: 1, Mode: Slider  
- **Name:** Hygger Blue Level
  - Min: 0, Max: 10, Step: 1, Mode: Slider

### Toggle Helper (Create 1)
- **Name:** Enable Aquarium Lightning
  - Icon: mdi:weather-lightning

### Text Helper (Create 1)
- **Name:** Aquarium Forecast Cache
  - Max length: 8192

## Step 5: Import Configurations

### Scripts
In Settings > Automations & Scenes > Scripts, create these scripts using the YAML files from the `scripts/` directory:
- `script.aquarium_reconcile_state`
- `script.aquarium_lightning_effect`
- `script.aquarium_reset_to_zero`
- `script.sync_aquarium_lights`

**Important:** Update the entity IDs in each script:
- Change `remote.rm4_pro_remote` to your actual Broadlink entity ID

### Automations
In Settings > Automations & Scenes > Automations, create these automations using the YAML files from the `automations/` directory:
- `automation.aquarium_dynamic_circadian_lighting`
- `automation.aquarium_daily_reset`
- `automation.aquarium_startup_sync`
- `automation.aquarium_forecast_caching`

**Important:** Update the entity IDs in the automations:
- Change `weather.openweathermap` to your actual weather entity ID
- Change `remote.rm4_pro_remote` to your actual Broadlink entity ID

## Step 6: Create Dashboard

1. **Create New Dashboard:**
   - Go to Settings > Dashboards
   - Click "Add Dashboard"
   - Name: "Aquarium Control"

2. **Configure Dashboard:**
   - Use the YAML from `dashboard/aquarium_control.yaml`
   - Update entity IDs to match your setup

## Step 7: Initial Sync

1. **Enable All Automations:**
   - Ensure all automations are turned on
   - Check that scripts are available

2. **Perform Initial Sync:**
   - Go to your Aquarium Control dashboard
   - Click the "Sync Lights" button
   - This will reset lights to zero and apply current state

## Step 8: Verification

Verify your setup is working:
- [ ] Light levels change based on time of day
- [ ] Weather affects lighting (cloudy = dimmer, etc.)
- [ ] Lightning effect works when enabled during storms
- [ ] Manual sync button works
- [ ] Daily reset happens at 2:00 AM
- [ ] System recovers after Home Assistant restart

## Troubleshooting

If something isn't working, check the [main README](README.md) troubleshooting section or create an issue in this repository.