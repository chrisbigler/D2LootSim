from flask import Flask, render_template, request, jsonify
import os
import json
import numpy as np
import sys

# Import DropSim from the same directory
# Add the current directory to Python path for Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from DropSim import ALL_GEAR_SLOTS, WEAPON_SLOTS, ARMOR_SLOTS
    import DropSim
except ImportError as e:
    # Try alternative import for Vercel environment
    try:
        from .DropSim import ALL_GEAR_SLOTS, WEAPON_SLOTS, ARMOR_SLOTS
        from . import DropSim
    except ImportError as e2:
        # If we still can't import, we'll define a minimal version
        print(f"Warning: Could not import DropSim: {e}, {e2}")
        ALL_GEAR_SLOTS = ["primary", "energy", "power", "helmet", "gloves", "chest", "legs", "class"]
        WEAPON_SLOTS = ["primary", "energy", "power"]
        ARMOR_SLOTS = ["helmet", "gloves", "chest", "legs", "class"]
        DropSim = None

app = Flask(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    'total_time_hours': 1.5,
    'starting_gear_level': 200
}

def convert_numpy_types(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj

@app.route('/')
def index():
    """Serve the main HTML file"""
    # Read and return the index.html file from the parent directory
    html_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    try:
        with open(html_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "index.html not found", 404

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    """Run simulation with user-provided parameters"""
    if DropSim is None:
        return jsonify({'success': False, 'error': 'DropSim module not available'})
    
    try:
        # Get parameters from request
        data = request.json
        system_name = data.get('system_name', 'solo')
        config = data.get('config', DEFAULT_CONFIG)
        
        # Extract configuration values
        total_time_hours = float(config.get('total_time_hours', 1.5))
        starting_gear_level = int(config.get('starting_gear_level', 200))
        streak_bonuses = config.get('streak_bonuses')
        drop_ranges = config.get('drop_ranges')
        
        # Thread-safe approach: temporarily set globals with a lock
        import threading
        lock = threading.Lock()
        
        with lock:
            # Store original values
            original_total_time = DropSim.TOTAL_TIME_HOURS
            original_starting_level = DropSim.STARTING_GEAR_LEVEL
            
            try:
                # Set new values
                DropSim.TOTAL_TIME_HOURS = total_time_hours
                DropSim.STARTING_GEAR_LEVEL = starting_gear_level
                
                # Run simulation
                drops, activities, gear_tracker, max_streak, streak_info = DropSim.run_sim(system_name, streak_bonuses, drop_ranges)
                summary = gear_tracker.get_summary()
                
                # Calculate progression metrics using the current config values
                levels_gained = summary['character_level'] - starting_gear_level
                levels_per_hour = levels_gained / total_time_hours if total_time_hours > 0 else 0
                levels_needed = 450 - summary['character_level']
                hours_to_max = levels_needed / levels_per_hour if levels_per_hour > 0 else float('inf')
                
            finally:
                # Always restore original values
                DropSim.TOTAL_TIME_HOURS = original_total_time
                DropSim.STARTING_GEAR_LEVEL = original_starting_level
        
        result = {
            'type': 'single',
            'system_name': system_name,
            'drops': drops,
            'activities': activities,
            'max_streak': max_streak,
            'character_level': summary['character_level'],
            'levels_gained': levels_gained,
            'levels_per_hour': levels_per_hour,
            'hours_to_max': hours_to_max if hours_to_max != float('inf') else None,
            'upgrade_rate': summary['upgrade_rate'],
            'total_upgrades': summary['total_upgrades'],
            'gear_levels': {
                'weapons': {slot: gear_tracker.gear_levels[slot] for slot in WEAPON_SLOTS},
                'armor': {slot: gear_tracker.gear_levels[slot] for slot in ARMOR_SLOTS}
            },
            'streak_info': streak_info
        }
        
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/compare_systems', methods=['POST'])
def compare_systems():
    """Compare all three systems with comprehensive analysis matching single run detail level"""
    if DropSim is None:
        return jsonify({'success': False, 'error': 'DropSim module not available'})
    
    try:
        data = request.json
        config = data.get('config', DEFAULT_CONFIG)
        
        # Extract configuration values
        total_time_hours = float(config.get('total_time_hours', 1.5))
        starting_gear_level = int(config.get('starting_gear_level', 200))
        streak_bonuses = config.get('streak_bonuses')
        drop_ranges = config.get('drop_ranges')
        
        # Thread-safe approach: temporarily set globals with a lock
        import threading
        lock = threading.Lock()
        
        # Use ordered dictionary to ensure correct system order: solo, fireteam, ,pinnacle
        from collections import OrderedDict
        results = OrderedDict()
        
        with lock:
            # Store original values
            original_total_time = DropSim.TOTAL_TIME_HOURS
            original_starting_level = DropSim.STARTING_GEAR_LEVEL
            
            try:
                # Set new values
                DropSim.TOTAL_TIME_HOURS = total_time_hours
                DropSim.STARTING_GEAR_LEVEL = starting_gear_level
                
                # Process systems in the desired order with comprehensive analysis
                for system_name in ['solo', 'fireteam', 'pinnacle']:
                    # Run statistical analysis with 1000 trials for precision
                    stats = DropSim.monte_carlo(system_name, trials=1000, streak_bonuses=streak_bonuses, drop_ranges=drop_ranges)
                    
                    # Run a representative single simulation for detailed breakdown
                    drops, activities, gear_tracker, max_streak, streak_info = DropSim.run_sim(system_name, streak_bonuses, drop_ranges)
                    summary = gear_tracker.get_summary()
                    
                    # Calculate progression metrics from averaged stats
                    avg_character_level = stats['gear']['character_level']['average']
                    avg_level_gains = stats['gear']['character_level_gains']['average']
                    avg_upgrade_rate = stats['gear']['upgrade_rate']['average']
                    avg_total_upgrades = stats['gear']['total_upgrades']['average']
                    
                    levels_per_hour = avg_level_gains / total_time_hours if total_time_hours > 0 else 0
                    levels_needed = 450 - avg_character_level
                    hours_to_max = levels_needed / levels_per_hour if levels_per_hour > 0 else float('inf')
                    
                    # Compile comprehensive results
                    results[system_name] = {
                        # Core metrics (averaged from 1000 runs)
                        'drops': round(stats['drops']['average'], 1),
                        'activities': round(stats['activities']['average'], 1),
                        'max_streak': round(stats['max_streak']['average'], 1),
                        'character_level': round(avg_character_level, 1),
                        'levels_gained': round(avg_level_gains, 1),
                        'levels_per_hour': round(levels_per_hour, 2),
                        'hours_to_max': round(hours_to_max, 1) if hours_to_max != float('inf') else None,
                        'upgrade_rate': round(avg_upgrade_rate, 3),
                        'total_upgrades': round(avg_total_upgrades, 1),
                        
                        # Statistical ranges for main metrics
                        'statistical_ranges': {
                            'drops': {
                                'min': stats['drops']['min'], 
                                'max': stats['drops']['max'], 
                                '95th_percentile': round(stats['drops']['95%_tile'], 1)
                            },
                            'activities': {
                                'min': stats['activities']['min'], 
                                'max': stats['activities']['max'], 
                                '95th_percentile': round(stats['activities']['95%_tile'], 1)
                            },
                            'character_level': {
                                'min': round(stats['gear']['character_level']['min'], 1), 
                                'max': round(stats['gear']['character_level']['max'], 1), 
                                '95th_percentile': round(stats['gear']['character_level']['95%_tile'], 1)
                            },
                            'upgrade_rate': {
                                'min': round(stats['gear']['upgrade_rate']['min'], 3), 
                                'max': round(stats['gear']['upgrade_rate']['max'], 3), 
                                '95th_percentile': round(stats['gear']['upgrade_rate']['95%_tile'], 3)
                            }
                        },
                        
                        # Analysis metadata
                        'trials': 1000,
                        'analysis_type': 'comprehensive',
                        'streak_info': streak_info
                    }
                
            finally:
                # Always restore original values
                DropSim.TOTAL_TIME_HOURS = original_total_time
                DropSim.STARTING_GEAR_LEVEL = original_starting_level
        
        return jsonify({'success': True, 'results': convert_numpy_types(results)})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# For Vercel serverless deployment
# The app variable is automatically used by Vercel's Python runtime
if __name__ == '__main__':
    app.run(debug=True)
