#!/usr/bin/env python3
"""
Quick test script to verify D2 Loot Sim setup
"""
import sys
import os
sys.path.append('api')

try:
    import DropSim
    print("✅ DropSim module imported successfully")
    
    # Test basic simulation
    drops, activities, gear_tracker, max_streak, streak_info = DropSim.run_sim('solo')
    print(f"✅ Solo simulation: {drops} drops, {activities} activities")
    
    # Test all systems
    for system in ['solo', 'fireteam', 'pinnacle']:
        result = DropSim.run_sim(system)
        print(f"✅ {system.capitalize()}: {result[0]} drops, {result[1]} activities, max streak: {result[3]}")
    
    print("\n🎉 All tests passed! Your D2 Loot Sim is ready to deploy!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")
