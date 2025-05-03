# algorithms/astar.py
import json
import heapq
import math
import os


def load_graph():
    """Load graph data with proper error handling"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '../nodesandedges/enhanced_campus_routes.json')
        
        with open(json_path) as f:
            data = json.load(f)
            
        # Convert edge format if needed
        if data['edges'] and isinstance(data['edges'][0], list):
            data['edges'] = [{
                'from': edge[0],
                'to': edge[1],
                'distance': edge[2] if len(edge) > 2 else 1.0,
                'time': edge[3] if len(edge) > 3 else 1.0,
                'has_stairs': edge[4] if len(edge) > 4 else False,
                'has_ramp': edge[5] if len(edge) > 5 else True
            } for edge in data['edges']]
            
        return data
    except Exception as e:
        print(f"Error loading graph: {str(e)}")
        return None

def heuristic(node1, node2, graph):
    """Euclidean distance heuristic for A*"""
    n1 = graph['nodes'][node1]
    n2 = graph['nodes'][node2]
    return math.sqrt((n2['x']-n1['x'])**2 + (n2['y']-n1['y'])**2)

def astar(graph, start, end, weight_type='distance'):
    nodes = {node['id']: node for node in graph['nodes']}
    edges = graph['edges']
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {node_id: float('infinity') for node_id in nodes}
    g_score[start] = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)
                current = came_from[current]
            path.insert(0, start)
            return path, g_score[end]
        
        # Get neighbors
        neighbors = []
        for edge in edges:
            if isinstance(edge, dict):
                from_node, to_node = edge['from'], edge['to']
                edge_data = edge
            else:
                from_node, to_node = edge[0], edge[1]
                edge_data = {
                    'distance': edge[2],
                    'time': edge[3],
                    'has_stairs': edge[4],
                    'has_ramp': edge[5]
                }
            
            if from_node == current:
                neighbors.append((to_node, edge_data))
            elif to_node == current:
                neighbors.append((from_node, edge_data))
        
        for neighbor, edge in neighbors:
            # Calculate tentative g_score
            if weight_type == 'time':
                weight = edge['time']
            elif weight_type == 'accessibility':
                weight = edge['distance'] * (2 if edge.get('has_stairs', False) else 1)
            else:
                weight = edge['distance']
                
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end, graph)
                heapq.heappush(open_set, (f_score, neighbor))
    
    return [], float('infinity')  # No path found



# def test_astar():
#     graph = load_graph()
#     if not graph:
#         print("Failed to load graph.")
#         return

#     print("Available locations (Node ID : Name):")
#     for node in graph['nodes']:
#         print(f"{node['id']:>2} : {node['name']}")

#     try:
#         start = int(input("\nEnter start node ID: ").strip())
#         end = int(input("Enter destination node ID: ").strip())
#     except ValueError:
#         print("Invalid input. Please enter numeric node IDs.")
#         return

#     if start not in [node['id'] for node in graph['nodes']] or end not in [node['id'] for node in graph['nodes']]:
#         print("Invalid node ID entered.")
#         return

#     print("\n=== A* Algorithm ===")
#     path, distance = astar(graph, start, end)
#     if path:
#         print(f"Shortest path from {graph['nodes'][start]['name']} to {graph['nodes'][end]['name']}:")
#         print(" -> ".join(graph['nodes'][node]['name'] for node in path))
#         print(f"Total distance: {distance:.2f} units")
#     else:
#         print("No path found.")

#     path, time = astar(graph, start, end, 'time')
#     if path:
#         print(f"\nFastest path (time):")
#         print(" -> ".join(graph['nodes'][node]['name'] for node in path))
#         print(f"Total time: {time:.2f} minutes")
#     else:
#         print("No path found.")

def test_astar():
    graph = load_graph()
    if not graph:
        print("Failed to load graph.")
        return

    print("Available locations (Node ID : Name):")
    for node in graph['nodes']:
        print(f"{node['id']:>2} : {node['name']}")

    try:
        start = int(input("\nEnter start node ID: ").strip())
        end = int(input("Enter destination node ID: ").strip())
    except ValueError:
        print("Invalid input. Please enter numeric node IDs.")
        return

    if start not in [node['id'] for node in graph['nodes']] or end not in [node['id'] for node in graph['nodes']]:
        print("Invalid node ID entered.")
        return

    start_name = graph['nodes'][start]['name']
    end_name = graph['nodes'][end]['name']
    print(f"\nTesting path from {start_name} to {end_name}:\n")

    # --- Best Distance Path ---
    path, distance = astar(graph, start, end, weight_type='distance')
    if path:
        print("Best distance path:")
        print(" -> ".join(f"{node} ({graph['nodes'][node]['name']})" for node in path) + " -> END")
        print(f"Total distance: {distance:.2f}\n")
    else:
        print("No path found for distance.\n")

    # --- Best Time Path ---
    path, time = astar(graph, start, end, weight_type='time')
    if path:
        print("Best time path:")
        print(" -> ".join(f"{node} ({graph['nodes'][node]['name']})" for node in path) + " -> END")
        print(f"Total time: {time:.2f}\n")
    else:
        print("No path found for time.\n")

    # --- Best Accessibility Path ---
    path, accessibility_score = astar(graph, start, end, weight_type='accessibility')
    if path:
        print("Best accessibility path:")
        print(" -> ".join(f"{node} ({graph['nodes'][node]['name']})" for node in path) + " -> END")
        print(f"Total accessibility: {accessibility_score:.2f}\n")
    else:
        print("No path found for accessibility.\n")



if __name__ == "__main__":
    test_astar()