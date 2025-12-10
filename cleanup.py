# resource_manager.py
import pandas as pd
# resource_manager.py
# import pandas as pd

def get_optimization_recommendations():
    """
    Analyzes resources for Right-Sizing (Downsizing suggestions).
    """
    # Mock Inventory with metrics
    # We merged "metrics" (cpu) with "instance info" (type)
    resources = [
        {"id": "i-1", "type": "t3.micro",   "cpu_avg": 80, "cost": 10}, # Good usage
        {"id": "i-2", "type": "m5.4xlarge", "cpu_avg": 2,  "cost": 500}, # BAD! Huge server, no work.
        {"id": "i-3", "type": "c5.large",   "cpu_avg": 5,  "cost": 85},  # BAD! Low usage.
    ]
    
    recommendations = []
    
    for res in resources:
        # --- HEURISTIC RULE 1: DOWNSIZING ---
        # If it's a big server but CPU is barely used (< 10%)
        if "xlarge" in res['type'] and res['cpu_avg'] < 10:
            savings = res['cost'] * 0.5 # Assume 50% saving
            rec = {
                "Resource": res['id'],
                "Issue": "Over-provisioned (Lazy Server)",
                "Action": f"Downsize from {res['type']} to Medium",
                "Potential Savings": f"${savings}/mo"
            }
            recommendations.append(rec)
            
        # --- HEURISTIC RULE 2: IDLE ---
        # If CPU is basically zero (< 3%)
        elif res['cpu_avg'] < 3:
             rec = {
                "Resource": res['id'],
                "Issue": "Ideally Idle",
                "Action": "Turn off at Night/Weekends",
                "Potential Savings": "variable"
            }
             recommendations.append(rec)

    return pd.DataFrame(recommendations)
def get_zombie_resources():
    """
    Scans for idle resources and returns the inventory and a list of zombies.
    """
    # Mock inventory: ID, State, Idle_Hours, Tags
    resources = [
        {"id": "i-123", "state": "running", "idle_hours": 2, "tags": {"owner": "dev"}},
        {"id": "i-456", "state": "running", "idle_hours": 5, "tags": {"owner": "test"}},
        {"id": "i-999", "state": "running", "idle_hours": 48, "tags": {}}, # No tags + Idle > 24h = BAD
    ]
    
    df = pd.DataFrame(resources)
    
    # Logic: Find resources idle > 24h AND no tags
    zombie_ids = []
    for res in resources:
        if res['idle_hours'] > 24 and not res['tags']:
            zombie_ids.append(res['id'])
            
    return df, zombie_ids