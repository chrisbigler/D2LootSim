import random
import numpy as np
from collections import defaultdict

# ------------------------------
# 1.  Configuration
# ------------------------------

# Gear Slots
WEAPON_SLOTS = ["primary", "energy", "power"]
ARMOR_SLOTS = ["helmet", "gloves", "chest", "legs", "class"]
ALL_GEAR_SLOTS = WEAPON_SLOTS + ARMOR_SLOTS

# Gear System
class GearTracker:
    def __init__(self):
        # Track current gear level for each slot (starts at configurable level)
        self.gear_levels = {slot: STARTING_GEAR_LEVEL for slot in ALL_GEAR_SLOTS}
        # Track total drops received for each slot
        self.drops_received = {slot: 0 for slot in ALL_GEAR_SLOTS}
        # Track drop history (slot, drop_level, was_upgrade)
        self.drop_history = []
    
    def get_character_level(self):
        """Calculate character level as average gear score rounded down, capped at 450"""
        if not self.gear_levels:
            return STARTING_GEAR_LEVEL
        average_level = sum(self.gear_levels.values()) / len(self.gear_levels)
        return min(450, int(average_level))  # Round down and cap at 450
    
    def apply_drop(self, activity_type="solo", drop_ranges=None):
        """Apply a gear drop: random slot, check if it's an upgrade"""
        slot = random.choice(ALL_GEAR_SLOTS)
        character_level = self.get_character_level()
        
        # Use configurable drop ranges if provided, otherwise use global defaults
        if drop_ranges and activity_type in drop_ranges:
            min_bonus, max_bonus = drop_ranges[activity_type]
        else:
            min_bonus, max_bonus = DROP_LEVEL_RANGES.get(activity_type, (1, 3))
        
        # Generate drop level: current char level + configurable range
        drop_level = character_level + random.randint(min_bonus, max_bonus)
        drop_level = min(450, drop_level)  # Cap at 450
        
        # Check if this is an upgrade
        was_upgrade = drop_level > self.gear_levels[slot]
        
        # Update slot if it's higher
        if was_upgrade:
            self.gear_levels[slot] = drop_level
        
        self.drops_received[slot] += 1
        self.drop_history.append((slot, drop_level, was_upgrade))
        
        return slot, drop_level, was_upgrade
    
    def get_total_power(self):
        """Get total power level across all gear"""
        return sum(self.gear_levels.values())
    
    def get_summary(self):
        """Get a summary of current gear state"""
        weapons = {slot: self.gear_levels[slot] for slot in WEAPON_SLOTS}
        armor = {slot: self.gear_levels[slot] for slot in ARMOR_SLOTS}
        
        # Count actual upgrades vs total drops
        total_upgrades = sum(1 for _, _, was_upgrade in self.drop_history if was_upgrade)
        total_drops = len(self.drop_history)
        
        return {
            "weapons": weapons,
            "armor": armor,
            "total_power": self.get_total_power(),
            "character_level": self.get_character_level(),
            "drops_received": dict(self.drops_received),
            "total_upgrades": total_upgrades,
            "total_drops": total_drops,
            "upgrade_rate": total_upgrades / total_drops if total_drops > 0 else 0
        }
OPERATION_TIMES = {
    "solo": (3, 5),      # solo ops take 3-5 minutes
    "fireteam": (8, 12), # fireteam ops take 8-12 minutes
    "pinnacle": None     # pinnacle ops have variable timing (handled in run_sim)
}

# Drop level ranges for each activity type (added above character level)
DROP_LEVEL_RANGES = {
    "solo": (1, 3),      # solo ops drop +1 to +3 above character level
    "fireteam": (1, 3),  # fireteam ops drop +1 to +3 above character level  
    "pinnacle": (1, 3),  # pinnacle ops drop +1 to +3 above character level
}

STARTING_GEAR_LEVEL = 200            # starting level for all gear pieces
TOTAL_TIME_HOURS = 10               # simulate for 10 hours (single play session length)

# Default systems configuration - Edge of Fated Leveling & Tiers Rework
# Updated to match the new system specifications from Google Sheets
DEFAULT_SYSTEMS = {
    "solo": {
        # Edge of Fated: No Streaks - Simplified reward structure
        # 1 Drop + Occasional Rotating Bonus Focus Slot Drops
        1: lambda: 1,  # No streak progression - always 1 drop
        2: lambda: 1,  # Maintained for compatibility but not used in new system
        3: lambda: 1,  # Maintained for compatibility but not used in new system
    },
    "fireteam": {
        # Updated default streak rewards
        1: lambda: 2,
        2: lambda: 3,
        3: lambda: 3,
    },
    "pinnacle": {
        # Updated default streak rewards
        1: lambda: 3,
        2: lambda: 4,
        3: lambda: 4,
    },
}

def calculate_max_achievable_streak(system_name, session_hours):
    """Calculate the maximum achievable streak based on session length and activity times"""
    if system_name == "pinnacle":
        # For pinnacle, all activities are exotic missions (10-20 min avg = 14.5 min)
        avg_activity_time = 14.5
    else:
        # For solo/fireteam, use average of time range
        time_range = OPERATION_TIMES[system_name]
        avg_activity_time = (time_range[0] + time_range[1]) / 2
    
    session_minutes = session_hours * 60
    
    # Calculate theoretical max consecutive activities in entire session
    max_activities = int(session_minutes / avg_activity_time)
    
    # Max streak is the smaller of: total activities possible in session, or 3 (hard cap)
    # No mid-session resets - streaks persist for the entire play session
    max_achievable_streak = min(max_activities, 3)
    
    # Ensure at least streak 1 is possible
    return max(1, max_achievable_streak)

def create_systems_from_config(streak_bonuses=None):
    """Create systems dictionary from streak bonus configuration"""
    if streak_bonuses is None:
        return DEFAULT_SYSTEMS
    
    systems = {}
    for system_name in ["solo", "fireteam", "pinnacle"]:
        if system_name in streak_bonuses:
            systems[system_name] = {}
            for streak_level in range(1, 4):
                # Handle both string and integer keys from JSON parsing
                streak_config = streak_bonuses[system_name]
                # Use None check instead of 'or' to properly handle 0 values
                drop_count = streak_config.get(streak_level)
                if drop_count is None:
                    drop_count = streak_config.get(str(streak_level), 1)
                systems[system_name][streak_level] = (lambda count: lambda: count)(drop_count)
        else:
            # Use default if not provided
            systems[system_name] = DEFAULT_SYSTEMS[system_name]
    
    return systems

# ------------------------------
# 2.  Single simulation run
# ------------------------------
def run_sim(system_name, streak_bonuses=None, drop_ranges=None):
    systems = create_systems_from_config(streak_bonuses)
    rules = systems[system_name]
    time_range = OPERATION_TIMES[system_name]
    total_time_min = TOTAL_TIME_HOURS * 60
    
    # Calculate dynamic max streak based on session length
    max_achievable_streak = calculate_max_achievable_streak(system_name, TOTAL_TIME_HOURS)
    
    # DIRECT CALCULATION APPROACH:
    # 1. Calculate total activities that can be completed in the given time
    # 2. Calculate drops based on activities completed and streak progression
    
    # Calculate total activities with slight variation for realism
    if system_name == "pinnacle":
        # Pinnacle ops: 10-15 min each, use random efficiency factor
        base_time_per_activity = 12.5  # Average time
        efficiency_factor = random.uniform(0.9, 1.1)  # ±10% variation
        avg_activity_time = base_time_per_activity * efficiency_factor
    else:
        # Solo/Fireteam ops: use time range with efficiency variation
        base_time_per_activity = (time_range[0] + time_range[1]) / 2
        efficiency_factor = random.uniform(0.85, 1.15)  # ±15% variation for player skill/luck
        avg_activity_time = base_time_per_activity * efficiency_factor
    
    # Calculate total activities possible in the session
    total_activities = int(total_time_min / avg_activity_time)
    
    # DIRECT CALCULATION: Calculate total drops based on activities and streak progression
    # This approach provides predictable results based on time investment and streak bonuses
    drops = 0
    gear_tracker = GearTracker()
    
    # Process each activity in the session, building up streak bonuses
    for activity_num in range(1, total_activities + 1):
        # Current streak level builds from 1 to max_achievable_streak based on activity number
        current_streak = min(activity_num, max_achievable_streak)
        
        # Calculate drops for this activity based on system type and current streak
        if system_name == "pinnacle":
            # Pinnacle ops: use streak-based drop rules with slight variation
            base_drops = rules[current_streak]()
            variation = random.randint(-1, 1)  # ±1 drop variation
            num_drops = max(0, base_drops + variation)
        else:
            # Solo/Fireteam ops: use streak-based drop rules
            num_drops = rules[current_streak]()
        
        drops += num_drops
        
        # Apply gear drops for progression tracking
        for _ in range(num_drops):
            gear_tracker.apply_drop(system_name, drop_ranges)
    
    # Maximum streak reached is the final streak level
    max_streak = min(total_activities, max_achievable_streak) if total_activities > 0 else 1
    
    # Include dynamic streak information
    streak_info = {
        'max_achievable_streak': max_achievable_streak,
        'session_hours': TOTAL_TIME_HOURS,
        'streak_reset_policy': 'session_only',  # Streaks only reset between play sessions
        'calculation_method': 'direct'  # New field to indicate calculation method
    }
    
    return drops, total_activities, gear_tracker, max_streak, streak_info

# ------------------------------
# 3.  Monte-Carlo envelope
# ------------------------------
def monte_carlo(system_name, trials=50_000, streak_bonuses=None, drop_ranges=None):
    results = [run_sim(system_name, streak_bonuses, drop_ranges) for _ in range(trials)]
    drops = np.array([r[0] for r in results])
    activities = np.array([r[1] for r in results])
    gear_trackers = [r[2] for r in results]
    max_streaks = np.array([r[3] for r in results])
    # Note: streak_info (r[4]) is the same for all runs, so we can ignore it in aggregation
    
    # Calculate gear statistics
    total_powers = np.array([gt.get_total_power() for gt in gear_trackers])
    character_levels = np.array([gt.get_character_level() for gt in gear_trackers])
    character_level_gains = character_levels - STARTING_GEAR_LEVEL  # Calculate level gains from starting point
    
    # Calculate per-slot statistics
    slot_stats = {}
    for slot in ALL_GEAR_SLOTS:
        slot_levels = np.array([gt.gear_levels[slot] for gt in gear_trackers])
        slot_drops = np.array([gt.drops_received[slot] for gt in gear_trackers])
        
        slot_stats[slot] = {
            "avg_level": slot_levels.mean(),
            "max_level": slot_levels.max(),
            "min_level": slot_levels.min(),
            "avg_drops": slot_drops.mean(),
            "95%_level": np.percentile(slot_levels, 95)
        }
    
    # Calculate upgrade statistics
    upgrade_rates = np.array([gt.get_summary()["upgrade_rate"] for gt in gear_trackers])
    total_upgrades = np.array([gt.get_summary()["total_upgrades"] for gt in gear_trackers])
    
    return {
        "drops": {
            "average": drops.mean(),
            "95%_tile": np.percentile(drops, 95),
            "min": drops.min(),
            "max": drops.max(),
        },
        "activities": {
            "average": activities.mean(),
            "95%_tile": np.percentile(activities, 95),
            "min": activities.min(),
            "max": activities.max(),
        },
        "max_streak": {
            "average": max_streaks.mean(),
            "95%_tile": np.percentile(max_streaks, 95),
            "min": max_streaks.min(),
            "max": max_streaks.max(),
        },
        "gear": {
            "total_power": {
                "average": total_powers.mean(),
                "95%_tile": np.percentile(total_powers, 95),
                "min": total_powers.min(),
                "max": total_powers.max(),
            },
            "character_level": {
                "average": character_levels.mean(),
                "95%_tile": np.percentile(character_levels, 95),
                "min": character_levels.min(),
                "max": character_levels.max(),
            },
            "character_level_gains": {
                "average": character_level_gains.mean(),
                "95%_tile": np.percentile(character_level_gains, 95),
                "min": character_level_gains.min(),
                "max": character_level_gains.max(),
            },
            "upgrade_rate": {
                "average": upgrade_rates.mean(),
                "95%_tile": np.percentile(upgrade_rates, 95),
                "min": upgrade_rates.min(),
                "max": upgrade_rates.max(),
            },
            "total_upgrades": {
                "average": total_upgrades.mean(),
                "95%_tile": np.percentile(total_upgrades, 95),
                "min": total_upgrades.min(),
                "max": total_upgrades.max(),
            },
            "slots": slot_stats
        }
    }

def print_single_run_results(system_name, streak_bonuses=None):
    """Run and display results for a single simulation"""
    print(f"=== SINGLE {system_name.upper()} RUN ===")
    drops, activities, gear_tracker, max_streak, streak_info = run_sim(system_name, streak_bonuses, None)
    summary = gear_tracker.get_summary()
    
    # Basic stats
    print(f"Total Drops: {drops}")
    print(f"Activities Completed: {activities}")
    print(f"Total Time: {TOTAL_TIME_HOURS} hours")
    print(f"Max Streak Reached: {max_streak}")
    print(f"Character Level: {summary['character_level']}")
    print(f"Upgrade Rate: {summary['upgrade_rate']:.1%}")
    print(f"Total Upgrades: {summary['total_upgrades']}")
    
    # Calculate progression rate and time to max level
    starting_level = STARTING_GEAR_LEVEL  # All gear starts at configurable level
    current_level = summary['character_level']
    levels_gained = current_level - starting_level
    
    if levels_gained > 0:
        # Calculate progression rates
        levels_per_hour = levels_gained / TOTAL_TIME_HOURS
        levels_per_activity = levels_gained / activities if activities > 0 else 0
        levels_per_drop = levels_gained / drops if drops > 0 else 0
        
        # Calculate time to reach max level (450)
        levels_needed = 450 - current_level
        
        if levels_needed <= 0:
            print(f"\n🎉 MAX LEVEL REACHED! Character is already at cap (450)!")
        else:
            hours_to_max = levels_needed / levels_per_hour if levels_per_hour > 0 else float('inf')
            activities_to_max = levels_needed / levels_per_activity if levels_per_activity > 0 else float('inf')
            drops_to_max = levels_needed / levels_per_drop if levels_per_drop > 0 else float('inf')
            
            print(f"\nPROGRESSION ANALYSIS:")
            print(f"Levels gained: {levels_gained} (from {starting_level} to {current_level})")
            print(f"Progression rate: {levels_per_hour:.2f} levels/hour, {levels_per_activity:.2f} levels/activity")
            
            print(f"\nTIME TO MAX LEVEL (450) AT THIS PACE:")
            print(f"Levels still needed: {levels_needed}")
            
            if hours_to_max < float('inf'):
                if hours_to_max < 1000:  # Only show if reasonable
                    print(f"Estimated time: {hours_to_max:.1f} hours ({hours_to_max/24:.1f} days)")
                    print(f"Estimated activities: {activities_to_max:.0f}")
                    print(f"Estimated drops: {drops_to_max:.0f}")
                else:
                    print(f"Estimated time: {hours_to_max:.0f}+ hours (very slow progression)")
            else:
                print("Unable to calculate - no progression detected")
    else:
        print(f"\nNo level progression detected (stayed at starting level {starting_level})")
    
    # Per-slot breakdown
    print(f"\nFINAL GEAR LEVELS:")
    for slot in ALL_GEAR_SLOTS:
        level = gear_tracker.gear_levels[slot]
        drops_count = gear_tracker.drops_received[slot]
        slot_type = "WEAPON" if slot in WEAPON_SLOTS else "ARMOR"
        print(f"  {slot:8s} ({slot_type}): Level {level:2d} ({drops_count:2d} drops)")
    
    # Level range analysis
    levels = list(gear_tracker.gear_levels.values())
    print(f"\nGear Level Range: {min(levels)} - {max(levels)} (spread: {max(levels) - min(levels)})")

def print_average_results(system_name, trials=100, streak_bonuses=None):
    """Run multiple simulations and show average results"""
    print(f"=== AVERAGE {system_name.upper()} RESULTS ({trials} runs) ===")
    stats = monte_carlo(system_name, trials=trials, streak_bonuses=streak_bonuses)
    drops = stats['drops']
    activities = stats['activities']
    gear = stats['gear']
    
    # Calculate time to max level ranges based on progression rates from 4-hour sessions
    time_estimates = []
    for _ in range(min(500, trials)):  # Sample runs to get progression rate variability
        test_drops, test_activities, test_gear_tracker, test_max_streak, test_streak_info = run_sim(system_name, streak_bonuses, None)
        current_level = test_gear_tracker.get_character_level()
        levels_gained = current_level - STARTING_GEAR_LEVEL
        
        if levels_gained > 0:  # Only calculate if there was progression
            levels_per_hour = levels_gained / TOTAL_TIME_HOURS
            levels_needed = 450 - current_level
            hours_to_max = levels_needed / levels_per_hour
            time_estimates.append(hours_to_max)
    
    # Basic averages
    print(f"Average Drops: {drops['average']:.1f}")
    print(f"Average Activities: {activities['average']:.1f}")
    print(f"Average Max Streak: {stats['max_streak']['average']:.1f}")
    print(f"Average Character Level: {gear['character_level']['average']:.1f}")
    print(f"Average Character Level Gained: {gear['character_level_gains']['average']:.1f}")
    print(f"Average Upgrade Rate: {gear['upgrade_rate']['average']:.1%}")
    print(f"Average Total Upgrades: {gear['total_upgrades']['average']:.1f}")
    
    # Character level progression analysis
    avg_level_gain = gear['character_level_gains']['average']
    if avg_level_gain > 0:
        levels_per_hour = avg_level_gain / TOTAL_TIME_HOURS
        levels_per_activity = avg_level_gain / activities['average'] if activities['average'] > 0 else 0
        print(f"\nPROGRESSION RATES:")
        print(f"Average levels gained per hour: {levels_per_hour:.2f}")
        print(f"Average levels gained per activity: {levels_per_activity:.3f}")
        
        # Calculate time to max level (450) at this pace
        current_avg_level = gear['character_level']['average']
        levels_needed = 450 - current_avg_level
        
        print(f"\nTIME TO MAX LEVEL (450):")
        if levels_needed <= 0:
            print(f"🎉 MAX LEVEL REACHED! Average character already at/above cap!")
        else:
            hours_to_max = levels_needed / levels_per_hour if levels_per_hour > 0 else float('inf')
            
            if hours_to_max < float('inf'):
                if hours_to_max < 1000:  # Only show if reasonable
                    print(f"Levels still needed: {levels_needed:.1f}")
                    print(f"Estimated time: {hours_to_max:.1f} hours ({hours_to_max/24:.1f} days)")
                    
                    # Show range information based on progression rate variability
                    if time_estimates:
                        avg_time_estimate = sum(time_estimates) / len(time_estimates)
                        min_time_estimate = min(time_estimates)
                        max_time_estimate = max(time_estimates)
                        print(f"Time range based on progression variability (from {len(time_estimates)} sessions): "
                              f"avg={avg_time_estimate:.1f}h range=({min_time_estimate:.1f}-{max_time_estimate:.1f}h)")
                    
                    # Calculate activities needed based on average activities per hour
                    activities_per_hour = activities['average'] / TOTAL_TIME_HOURS
                    activities_to_max = hours_to_max * activities_per_hour
                    print(f"Estimated activities: ~{activities_to_max:.0f}")
                else:
                    print(f"Estimated time: {hours_to_max:.0f}+ hours (very slow progression)")
            else:
                print("Unable to calculate - no progression detected")
    
    # Range information
    print(f"\nRANGES ACROSS {trials} RUNS:")
    print(f"Drops: {drops['min']}-{drops['max']}")
    print(f"Activities: {activities['min']}-{activities['max']}")
    print(f"Max Streak: {stats['max_streak']['min']}-{stats['max_streak']['max']}")
    print(f"Character Level: {gear['character_level']['min']}-{gear['character_level']['max']}")
    print(f"Character Level Gains: {gear['character_level_gains']['min']:.1f}-{gear['character_level_gains']['max']:.1f}")

def analyze_time_to_max_level(system_name, trials=1000, streak_bonuses=None):
    """Analyze how long it takes to reach maximum level (450)"""
    print(f"=== TIME TO MAX LEVEL ANALYSIS ({system_name.upper()}) ===")
    
    results = []
    max_level_reached = []
    time_estimates = []  # Track time estimates based on progression rates
    
    for _ in range(trials):
        drops, activities, gear_tracker, max_streak, streak_info = run_sim(system_name, streak_bonuses, None)
        final_level = gear_tracker.get_character_level()
        max_level_reached.append(final_level)
        levels_gained = final_level - STARTING_GEAR_LEVEL
        
        if levels_gained > 0:  # Calculate time estimate based on progression rate
            levels_per_hour = levels_gained / TOTAL_TIME_HOURS
            levels_needed = 450 - final_level
            hours_to_max = levels_needed / levels_per_hour
            time_estimates.append(hours_to_max)
        
        if final_level == 450:
            results.append((drops, activities))
    
    max_reached = max(max_level_reached)
    avg_reached = sum(max_level_reached) / len(max_level_reached)
    
    print(f"Results from {trials} simulations:")
    print(f"Highest level reached: {max_reached}")
    print(f"Average level reached: {avg_reached:.1f}")
    print(f"Runs that hit max level (450): {len(results)}/{trials} ({len(results)/trials:.1%})")
    
    # Calculate time statistics based on progression rate estimates
    if time_estimates:
        avg_time_hours = sum(time_estimates) / len(time_estimates)
        min_time_hours = min(time_estimates)
        max_time_hours = max(time_estimates)
        
        print(f"\nTO REACH MAX LEVEL (450):")
        print(f"Estimated time based on progression rates: {avg_time_hours:.1f} hours (range: {min_time_hours:.1f}-{max_time_hours:.1f})")
        
        if results:  # If any runs actually reached max level, show drop/activity stats too
            avg_drops = sum(r[0] for r in results) / len(results)
            avg_activities = sum(r[1] for r in results) / len(results)
            min_drops = min(r[0] for r in results)
            max_drops = max(r[0] for r in results)
            min_activities = min(r[1] for r in results)
            max_activities = max(r[1] for r in results)
            print(f"Average drops needed: {avg_drops:.1f} (range: {min_drops}-{max_drops})")
            print(f"Average activities needed: {avg_activities:.1f} (range: {min_activities}-{max_activities})")
    else:
        print(f"\nNOTE: No progression detected in any runs to calculate time estimates.")
        if not results:
            print(f"No runs reached max level in {TOTAL_TIME_HOURS} hours - estimates based on longer progression needed.")

def show_menu():
    """Display menu options"""
    print("="*60)
    print("DROPSIM ANALYSIS OPTIONS")
    print("="*60)
    print("1. Single run (Solo)")
    print("2. Single run (Fireteam)")
    print("3. Single run (Pinnacle Ops)")
    print("4. Average of 100 runs (Solo)")
    print("5. Average of 100 runs (Fireteam)")
    print("6. Average of 100 runs (Pinnacle Ops)")
    print("7. Time to max level analysis (Solo)")
    print("8. Time to max level analysis (Fireteam)")
    print("9. Time to max level analysis (Pinnacle Ops)")
    print("10. Full statistical analysis (Original)")
    print("11. Exit")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        # Interactive menu
        while True:
            show_menu()
            choice = input("Select option (1-11): ").strip()
            
            if choice == "11":
                print("Goodbye!")
                sys.exit(0)
            elif choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                break
            else:
                print("Invalid choice. Please select 1-11.\n")
    
    # Execute based on choice
    if choice == "1":
        print_single_run_results("solo")
    elif choice == "2":
        print_single_run_results("fireteam")
    elif choice == "3":
        print_single_run_results("pinnacle")
    elif choice == "4":
        print_average_results("solo", 100)
    elif choice == "5":
        print_average_results("fireteam", 100)
    elif choice == "6":
        print_average_results("pinnacle", 100)
    elif choice == "7":
        analyze_time_to_max_level("solo", 1000)
    elif choice == "8":
        analyze_time_to_max_level("fireteam", 1000)
    elif choice == "9":
        analyze_time_to_max_level("pinnacle", 1000)
    elif choice == "10":
        # Original full analysis
        for name in ["solo", "fireteam", "pinnacle"]:
            print(f"=== {name.upper()} OPERATIONS (FULL ANALYSIS) ===")
            stats = monte_carlo(name, trials=10000)
            drops = stats['drops']
            activities = stats['activities']
            max_streak = stats['max_streak']
            gear = stats['gear']
            
            # Calculate time to max level ranges based on progression rates from 4-hour sessions
            time_estimates = []
            for _ in range(1000):  # Sample runs to get progression rate variability
                test_drops, test_activities, test_gear_tracker, test_max_streak, test_streak_info = run_sim(name, None, None)
                current_level = test_gear_tracker.get_character_level()
                levels_gained = current_level - STARTING_GEAR_LEVEL
                
                if levels_gained > 0:  # Only calculate if there was progression
                    levels_per_hour = levels_gained / TOTAL_TIME_HOURS
                    levels_needed = 450 - current_level
                    hours_to_max = levels_needed / levels_per_hour
                    time_estimates.append(hours_to_max)
            
            # Basic drop and activity stats
            print(f"Drops:      avg={drops['average']:.1f}  95%≤{drops['95%_tile']:.1f} "
                  f"range=({drops['min']}, {drops['max']})")
            print(f"Activities: avg={activities['average']:.1f}  95%≤{activities['95%_tile']:.1f} "
                  f"range=({activities['min']}, {activities['max']})")
            print(f"Max Streak: avg={max_streak['average']:.1f}  95%≤{max_streak['95%_tile']:.1f} "
                  f"range=({max_streak['min']}, {max_streak['max']})")
            
            # Character level progression
            char_level = gear['character_level']
            print(f"Char Level:  avg={char_level['average']:.1f}  95%≤{char_level['95%_tile']:.1f} "
                  f"range=({char_level['min']}, {char_level['max']})")
            
            # Character level gains
            char_level_gains = gear['character_level_gains']
            print(f"Level Gains: avg={char_level_gains['average']:.1f}  95%≤{char_level_gains['95%_tile']:.1f} "
                  f"range=({char_level_gains['min']:.1f}, {char_level_gains['max']:.1f})")
            
            # Progression rates and time to max level
            if char_level_gains['average'] > 0:
                levels_per_hour = char_level_gains['average'] / TOTAL_TIME_HOURS
                print(f"Progression: {levels_per_hour:.2f} levels/hour average")
                
                # Calculate time to max level (450) at this pace
                current_avg_level = char_level['average']
                levels_needed = 450 - current_avg_level
                
                if levels_needed <= 0:
                    print(f"🎉 MAX LEVEL REACHED! Average character already at/above cap!")
                else:
                    hours_to_max = levels_needed / levels_per_hour if levels_per_hour > 0 else float('inf')
                    
                    if hours_to_max < float('inf'):
                        if hours_to_max < 1000:  # Only show if reasonable
                            print(f"Time to max level (450): {hours_to_max:.1f} hours ({hours_to_max/24:.1f} days)")
                            
                            # Show range information based on progression rate variability
                            if time_estimates:
                                avg_time_estimate = sum(time_estimates) / len(time_estimates)
                                min_time_estimate = min(time_estimates)
                                max_time_estimate = max(time_estimates)
                                print(f"Time range based on progression variability (from {len(time_estimates)} sessions): "
                                      f"avg={avg_time_estimate:.1f}h range=({min_time_estimate:.1f}-{max_time_estimate:.1f}h)")
                            
                            # Calculate activities needed based on average activities per hour
                            activities_per_hour = activities['average'] / TOTAL_TIME_HOURS
                            activities_to_max = hours_to_max * activities_per_hour
                            print(f"Activities needed: ~{activities_to_max:.0f}")
                        else:
                            print(f"Time to max level: {hours_to_max:.0f}+ hours (very slow progression)")
                    else:
                        print("Unable to calculate max level time - no progression detected")
            
            # Upgrade statistics
            upgrade_rate = gear['upgrade_rate']
            total_upgrades = gear['total_upgrades']
            print(f"Upgrade Rate: avg={upgrade_rate['average']:.2f}  95%≤{upgrade_rate['95%_tile']:.2f} "
                  f"range=({upgrade_rate['min']:.2f}, {upgrade_rate['max']:.2f})")
            print(f"Total Upgrades: avg={total_upgrades['average']:.1f}  95%≤{total_upgrades['95%_tile']:.1f} "
                  f"range=({total_upgrades['min']}, {total_upgrades['max']})")    
            
            print("\n" + "="*70 + "\n")
    else:
        print(f"Unknown option: {choice}")
        show_menu()