# Hygger HG016 Remote Command Troubleshooting Guide

## Problem Overview

This guide addresses issues where Hygger HG016 remote commands don't work as expected after learning them into the Broadlink RM4 Pro. Common symptoms include:

- `red_up` command shows no change
- `red_down` command shows teal instead of dimmer red
- `green_up` command shows teal instead of green
- `blue_down` command turns off lights instead of dimming blue

## Quick Diagnostic Tool

Run the diagnostic tool to get detailed analysis:

```bash
python3 diagnose_remote_commands.py
```

## Understanding the Issue

### Root Causes

1. **IR Learning Problems**: Commands may not have been captured correctly during the learning process
2. **Button Mislabeling**: Physical remote buttons may not correspond to their labels
3. **Hardware Variations**: Different Hygger HG016 batches may have different IR codes
4. **Interference**: Other IR devices or poor learning conditions

### Confirmed Working Commands
Based on user feedback, these commands work correctly:
- ✅ `white_up` → Bright white
- ✅ `white_down` → Dim white  
- ✅ `blue_up` → Bright blue

### Problematic Commands
These commands need troubleshooting:
- ❌ `red_up` → No change (should be bright red)
- ❌ `red_down` → Shows teal (should be dim red)
- ❌ `green_up` → Shows teal (should be bright green)
- ❌ `blue_down` → Turns off lights (should be dim blue)

## Step-by-Step Solution

### Phase 1: Delete Broken Commands

1. **Open Home Assistant Developer Tools**:
   - Go to Developer Tools > Actions
   - Search for "Remote: Delete command"

2. **Delete each broken command**:
   ```yaml
   service: remote.delete_command
   target:
     entity_id: remote.rm4_pro_remote  # Update to your entity
   data:
     device: hygger_hg016
     command: red_up
   ```
   
   Repeat for: `red_up`, `red_down`, `green_up`, `blue_down`

### Phase 2: Manual Button Testing

Before re-learning, test each physical button on the remote:

1. **Test Each Button Systematically**:
   - Press each button on the remote
   - Note the actual effect on the light
   - Create a mapping table:

   | Button Position | Actual Effect | Should Be Used For |
   |----------------|---------------|-------------------|
   | Top Left | ? | Document what happens |
   | Top Right | ? | Document what happens |
   | etc. | ? | Map all buttons |

2. **Look for These Effects**:
   - Button that increases red (use for `red_up`)
   - Button that decreases red (use for `red_down`)
   - Button that increases green (use for `green_up`)
   - Button that decreases blue without turning off (use for `blue_down`)

### Phase 3: Re-learn Commands

1. **Optimal Learning Conditions**:
   - Fresh remote batteries
   - Broadlink 6-12 inches from remote
   - No other IR devices nearby
   - Good lighting to see buttons clearly

2. **Learn Commands Based on Actual Button Effects**:
   
   ```yaml
   service: remote.learn_command
   target:
     entity_id: remote.rm4_pro_remote  # Update to your entity
   data:
     device: hygger_hg016
     command: red_up
   ```
   
   **Important**: Press the physical button that actually increases red color, not necessarily the button labeled for red.

3. **Learn All Problematic Commands**:
   - `red_up`: Button that makes light more red
   - `red_down`: Button that makes light less red
   - `green_up`: Button that makes light more green  
   - `blue_down`: Button that dims blue (doesn't turn off)

### Phase 4: Test New Commands

1. **Test Individual Commands**:
   ```yaml
   service: remote.send_command
   target:
     entity_id: remote.rm4_pro_remote  # Update to your entity
   data:
     device: hygger_hg016
     command: red_up
   ```

2. **Verify Expected Behavior**:
   - `red_up` should increase red intensity
   - `red_down` should decrease red intensity
   - `green_up` should increase green intensity 
   - `blue_down` should decrease blue intensity

3. **Run Complete Test**:
   Execute the "Aquarium Test Lights" script to verify all channels work correctly.

## Alternative Solutions

### Option 1: Custom Command Names

If standard commands don't work, create custom mappings:

```yaml
# Instead of red_up, use:
command: hygger_button_5  # Whatever actually works

# Update all scripts to use custom names
```

### Option 2: Modified Reset Script

If `blue_down` turns off lights, modify the reset script:

```yaml
# Replace blue_down commands with working alternative
# Or use white_down multiple times to ensure off state
```

### Option 3: Physical Remote Button Map

Create a custom button map based on your specific remote:

```yaml
# Example custom mapping
physical_button_1: white_up     # Top left
physical_button_2: white_down   # Top right  
physical_button_3: actual_red_up    # Based on testing
physical_button_4: actual_red_down  # Based on testing
# etc.
```

## Validation Commands

Use these Home Assistant actions to test:

### Test Commands
```yaml
service: remote.send_command
target:
  entity_id: remote.rm4_pro_remote
data:
  device: hygger_hg016
  command: [test_command_name]
```

### Learn Commands  
```yaml
service: remote.learn_command
target:
  entity_id: remote.rm4_pro_remote
data:
  device: hygger_hg016
  command: [new_command_name]
```

### Delete Commands
```yaml
service: remote.delete_command
target:
  entity_id: remote.rm4_pro_remote
data:
  device: hygger_hg016
  command: [bad_command_name]
```

## Hardware-Specific Notes

### Hygger HG016 (FCC ID: 2A6Qk-HG016)

- Some units may have non-standard button mappings
- IR codes may vary between manufacturing batches
- Remote may have unlabeled or multi-function buttons
- Consider contacting Hygger support for official IR documentation

### Broadlink RM4 Pro Considerations

- Ensure device is in learning mode when capturing commands
- Use stable power supply (not USB power from router)
- Keep device away from other IR sources during learning
- Consider factory reset if persistent issues occur

## Success Indicators

You'll know the issue is resolved when:

- ✅ All color channels respond to their respective commands
- ✅ "Aquarium Test Lights" script completes successfully
- ✅ Colors transition smoothly (white→red→green→blue)
- ✅ No unexpected color combinations (like teal when expecting red)
- ✅ Lights dim instead of turning off completely

## Getting Help

If this guide doesn't resolve your issue:

1. **Document Your Findings**:
   - Remote model and FCC ID
   - Physical button test results
   - Home Assistant version
   - Broadlink integration version

2. **Create Detailed Issue Report**:
   - Include the button mapping table you created
   - Note which solutions you've tried
   - Provide Home Assistant error logs if any

3. **Share Your Solution**:
   - If you find a working button mapping, share it
   - Help improve this documentation for other users
   - Consider submitting a pull request with your findings

## Files Updated by This Fix

When you find working commands, you may need to update:

- `scripts/aquarium_test_lights.yaml`
- `scripts/aquarium_reconcile_state.yaml`  
- `scripts/aquarium_reset_to_zero.yaml`
- `scripts/sync_aquarium_lights.yaml`
- `automations/aquarium_dynamic_circadian_lighting.yaml`

Replace the broken command names with your newly discovered working commands.