#!/usr/bin/env python3
"""
Hygger Remote Command Diagnostic Tool
Helps users identify and troubleshoot IR command mapping issues with the Hygger HG016 remote.
Based on user feedback about command behavior inconsistencies.
"""

import os
import sys

def print_header():
    """Print diagnostic tool header."""
    print("🔧 Hygger Remote Command Diagnostic Tool")
    print("=" * 60)
    print("This tool helps diagnose IR command mapping issues with")
    print("the Hygger HG016 remote (FCC ID: 2A6Qk-HG016)")
    print("=" * 60)
    print()

def print_expected_vs_actual():
    """Display the expected vs actual command behavior."""
    print("📋 EXPECTED vs ACTUAL Command Behavior")
    print("-" * 60)
    
    commands = [
        ("white_up", "Bright white", "✅ Bright white", "WORKING"),
        ("white_down", "Dim white", "✅ Dim white", "WORKING"),
        ("red_up", "Bright red", "❌ No change", "BROKEN"),
        ("red_down", "Dim red", "❌ Shows teal", "BROKEN"),
        ("green_up", "Bright green", "❌ Shows teal", "BROKEN"),
        ("green_down", "Dim green", "❓ Unknown", "UNKNOWN"),
        ("blue_up", "Bright blue", "✅ Shows blue", "WORKING"),
        ("blue_down", "Dim blue", "❌ Turns off lights", "BROKEN"),
    ]
    
    for cmd, expected, actual, status in commands:
        status_icon = "✅" if status == "WORKING" else "❌" if status == "BROKEN" else "❓"
        print(f"{status_icon} {cmd:12} | Expected: {expected:12} | Actual: {actual}")
    
    print()

def print_possible_causes():
    """Display possible causes and solutions."""
    print("🔍 POSSIBLE CAUSES AND SOLUTIONS")
    print("-" * 60)
    
    causes = [
        {
            "title": "1. IR Learning Issues",
            "description": "Commands may not have been learned correctly",
            "solutions": [
                "Re-learn all commands using the step-by-step process",
                "Ensure remote has fresh batteries",
                "Hold remote 6-12 inches from Broadlink device",
                "Press and hold remote buttons for 2-3 seconds during learning"
            ]
        },
        {
            "title": "2. Remote Button Confusion",
            "description": "Physical buttons on remote may be mislabeled or non-standard",
            "solutions": [
                "Try learning commands from different physical buttons",
                "Test each button individually to see actual effect",
                "Create a custom mapping based on actual button behavior"
            ]
        },
        {
            "title": "3. Hardware Interference",
            "description": "Multiple commands interfering with each other",
            "solutions": [
                "Increase delay between commands (use 500ms minimum)",
                "Test commands individually rather than in sequences",
                "Ensure no other IR devices are active during learning"
            ]
        },
        {
            "title": "4. Remote Firmware/Hardware Variant",
            "description": "Different Hygger HG016 variants may have different IR codes",
            "solutions": [
                "Try alternative command mappings (see suggestions below)",
                "Test with different learning sessions",
                "Contact Hygger support for IR code documentation"
            ]
        }
    ]
    
    for cause in causes:
        print(f"\n{cause['title']}:")
        print(f"   {cause['description']}")
        print("   Solutions:")
        for solution in cause['solutions']:
            print(f"   • {solution}")
    
    print()

def print_alternative_mappings():
    """Display alternative command mapping suggestions."""
    print("🔄 ALTERNATIVE COMMAND MAPPING SUGGESTIONS")
    print("-" * 60)
    print("Based on the reported behavior, try these alternative mappings:")
    print()
    
    print("ORIGINAL MAPPING ISSUES:")
    print("• red_up → no change")
    print("• red_down → shows teal")
    print("• green_up → shows teal") 
    print("• blue_down → turns off lights")
    print()
    
    print("SUGGESTED ALTERNATIVE MAPPINGS:")
    print("Try learning these physical buttons for the broken commands:")
    print()
    print("For RED channel:")
    print("• red_up: Try learning from the button that currently does 'no change'")
    print("• red_down: Try learning from a different button (not the teal one)")
    print()
    print("For GREEN channel:")
    print("• green_up: Try learning from a button other than the 'teal' one")
    print("• green_down: Test systematically with remaining buttons")
    print()
    print("For BLUE channel:")
    print("• blue_down: Try learning from any button except the 'off' one")
    print()
    print("SYSTEMATIC TESTING APPROACH:")
    print("1. Test each physical button and note its actual effect")
    print("2. Map the actual effects to the desired commands")
    print("3. Re-learn commands using the correct physical buttons")
    print()

def print_step_by_step_relearning():
    """Display detailed re-learning instructions."""
    print("📚 STEP-BY-STEP RE-LEARNING PROCESS")
    print("-" * 60)
    print()
    
    steps = [
        "1. Delete Existing Commands",
        "   • Go to Home Assistant > Developer Tools > Actions",
        "   • Use 'Remote: Delete command' for each broken command",
        "   • Device: hygger_hg016",
        "   • Commands to delete: red_up, red_down, green_up, blue_down",
        "",
        "2. Prepare for Re-learning",
        "   • Ensure Broadlink RM4 Pro is online and responsive",
        "   • Replace remote batteries if they're low",
        "   • Clear the area of other IR devices",
        "   • Have good lighting to see remote buttons clearly",
        "",
        "3. Test Each Button First",
        "   • Before learning, test each button manually",
        "   • Note what each button actually does to the light",
        "   • Create a map: Button Position → Actual Effect",
        "",
        "4. Learn Commands Based on Actual Effects",
        "   • Go to Developer Tools > Actions > 'Remote: Learn command'",
        "   • Device: hygger_hg016",
        "   • Learn commands using buttons that produce the desired effect:",
        "     - red_up: Use button that makes light more red",
        "     - red_down: Use button that makes light less red", 
        "     - green_up: Use button that makes light more green",
        "     - blue_down: Use button that makes light less blue (not off)",
        "",
        "5. Test New Commands",
        "   • Use Developer Tools > Actions > 'Remote: Send command'",
        "   • Test each newly learned command individually",
        "   • Verify the light responds as expected",
        "",
        "6. Run Full Test Sequence",
        "   • Execute the 'Aquarium Test Lights' script",
        "   • Observe if all color channels work correctly",
        "   • Note any remaining issues for further troubleshooting"
    ]
    
    for step in steps:
        print(step)
    
    print()

def print_diagnostic_commands():
    """Display Home Assistant diagnostic commands."""
    print("🔧 HOME ASSISTANT DIAGNOSTIC COMMANDS")
    print("-" * 60)
    print("Use these commands in Developer Tools > Actions to test:")
    print()
    
    print("TEST INDIVIDUAL COMMANDS:")
    print("Service: remote.send_command")
    print("Entity: remote.rm4_pro_remote  # (update to your actual entity)")
    print("Data:")
    print("  device: hygger_hg016")
    print("  command: [command_name]")
    print()
    
    print("DELETE BROKEN COMMANDS:")
    print("Service: remote.delete_command") 
    print("Entity: remote.rm4_pro_remote  # (update to your actual entity)")
    print("Data:")
    print("  device: hygger_hg016")
    print("  command: [command_name]")
    print()
    
    print("LEARN NEW COMMANDS:")
    print("Service: remote.learn_command")
    print("Entity: remote.rm4_pro_remote  # (update to your actual entity)")
    print("Data:")
    print("  device: hygger_hg016")
    print("  command: [command_name]")
    print()

def print_troubleshooting_checklist():
    """Display troubleshooting checklist."""
    print("✅ TROUBLESHOOTING CHECKLIST")
    print("-" * 60)
    
    checklist = [
        "□ Broadlink RM4 Pro is online and responding",
        "□ Remote has fresh batteries",
        "□ All existing broken commands have been deleted",
        "□ Each physical button has been tested manually",
        "□ Button-to-effect mapping has been documented",
        "□ Commands re-learned using correct physical buttons",
        "□ Individual commands tested via Developer Tools",
        "□ Full test sequence runs without issues",
        "□ All color channels respond as expected",
        "□ No interference from other IR devices"
    ]
    
    for item in checklist:
        print(item)
    
    print()
    print("📞 If issues persist after completing this checklist:")
    print("• Create a detailed issue report with:")
    print("  - Exact remote model and FCC ID")
    print("  - Home Assistant and Broadlink integration versions")
    print("  - Step-by-step test results")
    print("  - Photos of the remote (if helpful)")

def main():
    """Main diagnostic function."""
    print_header()
    print_expected_vs_actual()
    print_possible_causes()
    print_alternative_mappings()
    print_step_by_step_relearning()
    print_diagnostic_commands()
    print_troubleshooting_checklist()
    
    print("=" * 60)
    print("🎯 Next Steps:")
    print("1. Follow the step-by-step re-learning process above")
    print("2. Test systematically using the diagnostic commands")
    print("3. Update this repository if you find a working solution")
    print("4. Share your findings to help other users")
    print("=" * 60)

if __name__ == "__main__":
    main()