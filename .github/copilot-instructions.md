# Copilot Instructions for Dynamic Aquarium Lighting Project

## Project Overview

This repository contains a complete Home Assistant automation system for controlling Hygger HG016 aquarium lighting with dynamic, weather-aware circadian rhythm simulation. The system uses a Broadlink RM4 Pro IR blaster to control the lights based on time of day, weather conditions, and user preferences.

## Technologies & Architecture

- **Home Assistant**: Core automation platform running on Proxmox VM
- **YAML Configuration**: Automations, scripts, helpers, and dashboard configs
- **Python**: Validation scripts and diagnostic tools
- **Hardware**: Broadlink RM4 Pro IR blaster, Hygger HG016 LED lights
- **APIs**: OpenWeatherMap for weather data

## Key Components

### Configuration Files
- `automations/` - Home Assistant automation YAML files
- `scripts/` - Home Assistant script YAML files
- `helpers/` - Input helper configurations (numbers, booleans, text)
- `dashboard/` - Dashboard YAML configuration

### Python Tools
- `validate_config.py` - YAML syntax validation
- `check_entities.py` - Entity ID configuration checker
- `diagnose_lighting.py` - Diagnostic tool for troubleshooting
- `test_lights.py` - Light testing simulation

## Coding Guidelines

### YAML Configuration Files
- **Always validate YAML syntax** using `python3 validate_config.py` before committing
- **Entity ID patterns**:
  - Broadlink remote: `remote.rm4_pro_remote` (update to match user's actual device)
  - Weather: `weather.openweathermap` (update to match user's integration)
  - Helper entities follow `input_number.hygger_*_level` pattern
- **Maintain consistent formatting**: 2-space indentation, no tabs
- **Include meaningful descriptions** in automation and script configurations

### Python Scripts
- **Follow PEP 8** style guidelines
- **Include docstrings** for all functions and modules
- **Use meaningful variable names** that reflect Home Assistant concepts
- **Handle errors gracefully** with try/catch blocks for YAML parsing
- **Provide user-friendly output** with emojis and clear messaging

### Entity Management
- **Helper Entities Required**:
  - `input_number.hygger_white_level` (0-10 range)
  - `input_number.hygger_red_level` (0-10 range)
  - `input_number.hygger_green_level` (0-10 range)
  - `input_number.hygger_blue_level` (0-10 range)
  - `input_boolean.enable_aquarium_lightning`
  - `input_text.aquarium_forecast_cache`

### Testing & Validation
- **Run validation before commits**: Always use `python3 validate_config.py`
- **Test entity configurations**: Use `python3 check_entities.py`
- **Manual testing**: Use the light test script to verify IR commands
- **Check automation logic**: Verify time-based conditions and weather integration

## Common Patterns

### IR Command Structure
```yaml
service: remote.send_command
target:
  entity_id: remote.rm4_pro_remote  # Update to actual device
data:
  device: hygger_hg016
  command: white_up  # or white_down, red_up, etc.
```

### State Management
The system maintains virtual state using input helpers to track actual light levels since the Hygger light doesn't report its state back to Home Assistant.

### Weather Integration
- Caches forecasts in `input_text.aquarium_forecast_cache`
- Handles API outages gracefully
- Adjusts lighting based on cloud cover and weather conditions

## Troubleshooting Guide

### Common Issues
1. **Lights not responding**: Check Broadlink connectivity and IR command learning
2. **Wrong entity IDs**: Update `remote.rm4_pro_remote` and `weather.openweathermap`
3. **Missing helpers**: Ensure all input helpers are created in Home Assistant
4. **Automation errors**: Check Home Assistant logs for detailed error messages

### Diagnostic Tools
- Use `python3 diagnose_lighting.py` for comprehensive troubleshooting
- Check automation states in Home Assistant
- Verify weather API integration is working
- Test IR commands manually through Developer Tools

## File Organization

- **Active configurations**: Use files in root-level directories (`automations/`, `scripts/`, etc.)
- **Legacy/backup**: Old configurations are kept in `Old */` directories
- **Documentation**: `README.md`, `SETUP_GUIDE.md`, `TROUBLESHOOTING.md`
- **Tools**: Python scripts in root directory

## Best Practices for Contributors

1. **Test locally first**: Use the validation and diagnostic scripts
2. **Update documentation**: Modify relevant .md files for significant changes
3. **Maintain backward compatibility**: Don't break existing entity references
4. **Follow the stateful pattern**: Track virtual light state in helpers
5. **Handle edge cases**: Account for network outages, API failures, etc.
6. **Keep it user-friendly**: Provide clear error messages and setup instructions

## Validation Workflow

Always run these checks before committing changes:
```bash
# 1. Validate all YAML syntax
python3 validate_config.py

# 2. Check entity configurations (optional)
python3 check_entities.py

# 3. Test light functionality (if hardware available)
python3 test_lights.py
```

## Development Environment

### Required Dependencies
- Python 3.x with PyYAML library
- Home Assistant instance for testing
- Access to validation scripts in repository root

### .gitignore Considerations
The repository includes standard exclusions for:
- Python cache files (`__pycache__/`, `*.pyc`)
- OS-specific files (`.DS_Store`, `Thumbs.db`)
- Editor files (`*.swp`, `*.swo`)
- Temporary files (`*.tmp`, `*.temp`)

## Integration Notes

When modifying this system:
- **Entity IDs are user-configurable**: Always reference the need to update device-specific IDs
- **Weather API has rate limits**: Respect caching mechanisms
- **IR commands must be learned**: Each installation requires teaching the Broadlink the remote commands
- **Time calculations matter**: Circadian lighting depends on precise time-based logic
- **State synchronization is critical**: The system must recover gracefully from restarts
- **Automation timing**: Main automation runs every minute - be mindful of performance impact
- **Error handling**: All automations include fallback logic for network/API failures

## Quick Reference

### Key Automation Files
- `aquarium_dynamic_circadian_lighting.yaml` - Main lighting controller (runs every minute)
- `aquarium_daily_reset.yaml` - Daily state synchronization (2:00 AM)
- `aquarium_startup_sync.yaml` - Recovery after Home Assistant restart
- `aquarium_forecast_caching.yaml` - Weather data management

### Key Script Files  
- `sync_aquarium_lights.yaml` - Manual synchronization trigger
- `aquarium_reset_to_zero.yaml` - Reset all lights to off state
- `aquarium_lightning_effect.yaml` - Thunderstorm simulation
- `aquarium_test_lights.yaml` - Hardware validation script

This system is designed to be robust, user-friendly, and easily adaptable to different hardware configurations while maintaining the core weather-aware circadian lighting functionality.