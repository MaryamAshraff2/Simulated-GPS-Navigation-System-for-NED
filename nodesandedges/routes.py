# routes.py (fixed version)
import json

# Load your points - handles both formats
with open("map_points.json") as f:
    data = json.load(f)
    
# Handle either format:
if isinstance(data, list):
    # Old format: direct list of points
    nodes = data
else:
    # New format: dictionary with "points" key
    nodes = data["points"]

# Define meaningful names for each node (you should customize these)
node_names = [
    "Main Gate",            # 0
    "Car Park",       # 1
    "ATM",     # 2
    "DMS",     # 3
    "Roundabout ", # 4
    "Gymnasium",       # 5
    "Visitor's Gate",       # 6
    "Admission Center",   # 7
    "Food Centre",        # 8
    "Urban Dept",           # 9
    "Staff Centre",         # 10
    "Medical Department",         # 11
    "Electrical Dept",      # 12
    "Automative Dept",           # 13
    "Electronic Dept",          # 14
    "Mech Dept",       # 15
    "Old CIS-Labs",          # 16
    "Dean Office",     # 17
    "Library",           # 18
    "Metallurgy Dept",    # 19
    "Computing Centre",     # 20
    "Env Dept",      # 21
    "CIS",              # 22
    "Boys Hostel",          # 23
    "Maskan Gate",       # 24
    "Staff-colony Gate",           # 25
    "Colony"     # 26
]


# Define connections with additional properties
edges = [
    # Format: [from, to, distance_weight,
    #  time_weight, has_shade, less_crowded]
    [0, 1, 262.03, 2.0, False, True],
    [1, 2, 82.22, 1.5, False, True],
    [2, 3, 90.01, 2.2, False, False],
    [3, 4, 68.18, 1.8, False, False],
    [4, 5, 202.04, 2.0, True, True],
    [0, 6, 275.50, 3.0, True, True],
    [6, 7, 222.08, 1.3, False, True],
    [7, 8, 85.38, 1.2, False, True],
    [8, 9, 86.15, 1.0, False, True],
    [9, 10, 96.13, 1.6, True, True],
    [1, 7, 263.01, 1.7, False, True],
    [2, 8, 271.01, 1.9, True, False], 
    [3, 9, 277.04, 2.1, False, False],
    [4, 10, 277.04, 2.5, False, False],  
    [4, 13, 111.99, 2.7, False, False], 
    [10, 11, 119.07, 1.4, False, True],
    [11, 12, 125.00, 1.8, True, True], #done
    [12, 13, 144.07, 1.0, True, True],
    [13, 14, 119.07, 2.3, False, True],
    [11, 17, 129, 1.6, False, True],
    [14, 15, 57, 1.2, False, True],
    [15, 16, 74.01, 0.8, False, True],
    [16, 17, 102.06, 1.4, False, True],
    [16, 12, 127.02, 1.8, False, True],
    [17, 18, 139.00, 3.0, False, True],
    [18, 19, 105.08, 1.8, False, True],
    [19, 20, 89, 2.0, False, True],
    [20, 21, 54.59, 1.6, False, True],
    [21, 22, 185.00, 1.4, False, True],
    [14, 21, 125.00, 2.5, True, False],
    [15, 20, 136.02, 2.2, False, True],
    [16, 19, 130.02, 2.4, False, True],
    [18, 26, 257.12, 2.0, False, True],
    [23, 24, 173.23, 1.6, False, True],
    [24, 25, 89.05, 1.0, False, True],
    [25, 26, 150.00, 1.4, False, True],
    [24, 21, 269.48, 2.3, True, True],
    [20, 25, 266.66, 2.0, False, True],
    [23, 22, 263.95, 1.8, False, True]
]

# Save the enhanced routes
with open("enhanced_campus_routes.json", "w") as f:
    json.dump({
        "nodes": [{"id": i, "x": node[0], "y": node[1], "name": name} 
                 for i, (node, name) in enumerate(zip(nodes, node_names))],
        "edges": edges
    }, f, indent=2)

print(f"Created enhanced_campus_routes.json with {len(nodes)} named nodes and {len(edges)} weighted connections")