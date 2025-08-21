# DropSim.py - Gear Drop Simulation Documentation

## Overview

`DropSim.py` is a Monte Carlo simulation system that models gear progression in a video game with a loot-based character advancement system. The simulation tracks how players acquire and upgrade equipment over time through repeatable activities, using realistic drop mechanics and progression systems.

## Core Concepts

### Drop Calculation Method

The simulation uses a **direct calculation approach** for determining drops:

**Formula**: `Total Drops = Σ(drops_per_activity[streak_level]) for each activity in session`

**Process**:
1. **Calculate Activities**: `total_activities = session_time / avg_activity_time`
2. **Apply Efficiency**: Activity time includes ±10-15% variation for realism
3. **Progressive Streaks**: Each activity builds streak level (1→2→3→max)
4. **Sum Drops**: For each activity, add drops based on current streak level

**Benefits**:
- **Predictable**: Results are mathematically consistent
- **Time-based**: Directly correlates with time invested
- **Streak-aware**: Rewards sustained play sessions
- **Efficient**: No time-loop simulation overhead

### Gear System

The simulation models a character with **8 equipment slots**:

**Weapon Slots (3):**
- `primary` - Primary weapon slot
- `energy` - Energy weapon slot  
- `power` - Power weapon slot

**Armor Slots (5):**
- `helmet` - Head armor
- `gloves` - Hand armor
- `chest` - Chest armor
- `legs` - Leg armor
- `class` - Class item

### Character Progression

- **Starting Power**: All gear slots begin at level 200 (configurable via `STARTING_GEAR_LEVEL`)
- **Character Level**: Calculated as the average of all gear levels (rounded down), capped at 450
- **Drop Mechanics**: New gear drops at character level + 1-3 random bonus, capped at 450
- **Upgrade Logic**: Gear only improves if the dropped item is higher level than current equipment in that slot

## Activity Types

The simulation supports two types of activities with different time investments and reward structures:

### Solo Operations
- **Duration**: 3-5 minutes per activity
- **Streak Progression**:
  - Streak 1-2: 1 drop guaranteed
  - Streak 3-4: 2 drops guaranteed  
  - Streak 5: 3 drops guaranteed

### Fireteam Operations
- **Duration**: 8-12 minutes per activity
- **Streak Progression**:
  - Streak 1: 3 drops guaranteed
  - Streak 2: 4 drops guaranteed
  - Streak 3: 5 drops + 33% chance for bonus drop
  - Streak 4: 6 drops + 66% chance for bonus drop
  - Streak 5: 7 drops + 50% chance for bonus drop

## Simulation Parameters

### Configurable Settings
```python
STARTING_GEAR_LEVEL = 200         # Starting level for all gear pieces
TOTAL_TIME_HOURS = 4              # Simulation duration (4 hours)
```

### Streak System
- Streaks increment after each successful activity (1 → 2 → 3 → 4 → 5)
- At streak 5, all successive completions stay at that bonus level

## Key Classes and Functions

### `GearTracker` Class

The core class that maintains character progression state:

**Key Methods:**
- `get_character_level()`: Calculates current character level
- `apply_drop()`: Processes a single gear drop
- `get_total_power()`: Returns sum of all gear levels
- `get_summary()`: Provides comprehensive progression statistics

**Tracking Data:**
- Current gear level for each slot
- Total drops received per slot
- Complete drop history with upgrade tracking
- Upgrade rate calculations

### `run_sim(system_name)` Function

Executes a single simulation run using direct calculation approach:

1. **Activity Calculation**: Directly calculates total activities possible within the time period
2. **Efficiency Variation**: Applies realistic efficiency factors for player skill/luck variation
3. **Streak Progression**: Builds up streak bonuses progressively through the session
4. **Drop Calculation**: Calculates total drops as a direct function of activities and streaks
5. **Gear Progression**: Updates character equipment through `GearTracker`

**Key Improvement**: The simulation now uses a **direct calculation method** where the number of drops is a mathematical function of:
- Activities completed within the given time
- Streak bonuses accumulated during the play session
- System-specific drop rates

This provides more predictable and consistent results while maintaining realistic variation.

### `monte_carlo(system_name, trials)` Function

Performs statistical analysis across multiple simulation runs:

**Default Parameters**: 50,000 trials for robust statistical confidence

**Output Statistics:**
- **Drop Analysis**: Average, 95th percentile, min/max drops received
- **Activity Count**: Number of operations completed
- **Gear Progression**: Total power and character level progression
- **Character Level Gains**: Progression from starting level to final level
- **Upgrade Metrics**: Upgrade rates and total successful upgrades
- **Per-Slot Analysis**: Individual equipment slot progression tracking

### Analysis Functions

The simulation now provides multiple analysis modes for different use cases:

#### `print_single_run_results(system_name)`
Executes and displays results for a single simulation run, including:
- Basic progression statistics (drops, activities, character level)
- Progression rate analysis (levels per hour, per activity)
- Time-to-max-level estimates
- Per-slot gear breakdown with drop counts
- Gear level range analysis

#### `print_average_results(system_name, trials)`
Runs multiple simulations and shows averaged results:
- Average drops, activities, and character progression
- Progression rates across multiple runs
- Range information showing variability across trials
- Default: 100 trials for balanced accuracy and performance

#### `analyze_time_to_max_level(system_name, trials)`
Specialized analysis for understanding progression to maximum level (450):
- Percentage of runs that reach max level within time limit
- Statistics for successful max-level runs (drops/activities/time needed)
- Progression analysis for runs that don't reach max level
- Default: 1000 trials for statistical significance

## Statistical Output

The simulation provides comprehensive statistics for both activity types:

### Primary Metrics
- **Drops**: Total gear items received
- **Activities**: Number of activities completed
- **Character Level**: Average gear score (capped at 450)
- **Character Level Gains**: Progression from starting level (200) to final level
- **Upgrade Rate**: Percentage of drops that were actual improvements
- **Total Upgrades**: Count of successful gear improvements
- **Progression Rate**: Levels gained per hour and per activity
- **Time to Max Level**: Estimated time needed to reach level 450 based on current progression

### Per-Slot Analysis
For each of the 8 equipment slots:
- Average final gear level
- 95th percentile level achieved
- Level range (min/max)
- Average number of drops received

### Enhanced Single-Run Output
Individual simulation runs now provide detailed analysis including:
- **Progression Analysis**: Levels gained per hour and per activity
- **Time Estimates**: Projected time to reach maximum level (450) at current pace
- **Gear Breakdown**: Final level and drop count for each equipment slot
- **Gear Range Analysis**: Spread between highest and lowest gear pieces
- **Upgrade Efficiency**: Rate at which drops result in actual improvements

## Practical Applications

This simulation is valuable for:

1. **Game Balance**: Testing reward systems before implementation
2. **Player Experience**: Predicting progression rates and time investment
3. **Economic Modeling**: Understanding loot economy dynamics
4. **Feature Testing**: Evaluating impact of streak systems, etc.
5. **Statistical Analysis**: Providing data-driven insights for game design decisions

## Usage

The simulation supports both interactive menu mode and command-line execution:

### Interactive Menu Mode
```bash
python DropSim.py
```

This launches an interactive menu with the following options:
1. **Single run (Solo)** - Single simulation of solo operations
2. **Single run (Fireteam)** - Single simulation of fireteam operations  
3. **Average of 100 runs (Solo)** - Statistical average across 100 solo runs
4. **Average of 100 runs (Fireteam)** - Statistical average across 100 fireteam runs
5. **Time to max level analysis (Solo)** - Analysis of progression to level 450 (solo)
6. **Time to max level analysis (Fireteam)** - Analysis of progression to level 450 (fireteam)
7. **Full statistical analysis (Original)** - Comprehensive 10,000-trial analysis for both modes
8. **Exit** - Quit the program

### Command Line Mode
```bash
# Run specific analysis directly
python DropSim.py 1    # Single solo run
python DropSim.py 2    # Single fireteam run
python DropSim.py 3    # Average solo results
python DropSim.py 4    # Average fireteam results
python DropSim.py 5    # Solo time-to-max analysis
python DropSim.py 6    # Fireteam time-to-max analysis
python DropSim.py 7    # Full statistical analysis
```

The simulation demonstrates how different activity types create distinct risk/reward profiles, helping players and developers understand optimal strategies for character progression.

## Technical Implementation

- **Monte Carlo Method**: Uses random sampling to model complex probabilistic systems
- **Numpy Integration**: Leverages numpy for efficient statistical calculations
- **Realistic Modeling**: Time constraints and random variations mirror actual gameplay
- **Comprehensive Tracking**: Maintains detailed history for post-analysis
- **Interactive Interface**: Menu-driven system for easy analysis selection
- **Command Line Support**: Direct execution of specific analysis types via arguments
- **Multiple Analysis Modes**: Single runs, averaged results, and specialized time-to-max analysis

This simulation provides a robust framework for analyzing gear progression systems and can be easily modified to test different game mechanics, reward structures, or progression curves.