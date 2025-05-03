import json
import heapq
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
                'has_shade': edge[4] if len(edge) > 4 else False,
                'less_crowd': edge[5] if len(edge) > 5 else False
            } for edge in data['edges']]
            
        return data
    except Exception as e:
        print(f"Error loading graph: {str(e)}")
        return None

def comfort_dijkstra(graph, start, end, prefer_shade=False, prefer_less_crowded=False):
    """
    Dijkstra's variant that prioritizes shaded and less crowded paths based on user preferences
    """
    nodes = {node['id']: node for node in graph['nodes']}
    edges = graph['edges']
    
    heap = []
    heapq.heappush(heap, (0, start))
    
    prev_nodes = {start: None}
    costs = {node_id: float('infinity') for node_id in nodes}
    costs[start] = 0
    
    while heap:
        current_cost, current_node = heapq.heappop(heap)
        
        if current_node == end:
            break
            
        if current_cost > costs[current_node]:
            continue
            
        for edge in edges:
            if isinstance(edge, dict):
                from_node, to_node = edge['from'], edge['to']
                edge_data = edge
            else:
                from_node, to_node = edge[0], edge[1]
                edge_data = {
                    'distance': edge[2],
                    'has_shade': edge[4] if len(edge) > 4 else False,
                    'less_crowd': edge[5] if len(edge) > 5 else False
                }
            
            neighbor = None
            if from_node == current_node:
                neighbor = to_node
            elif to_node == current_node:
                neighbor = from_node
            else:
                continue
                
            # Calculate cost based on preferences
            base_cost = edge_data['distance']
            comfort_factor = 1.0
            
            if prefer_shade and not edge_data.get('has_shade', False):
                comfort_factor *= 1.5  # Penalize unshaded paths
                
            if prefer_less_crowded and not edge_data.get('less_crowd', False):
                comfort_factor *= 1.3  # Penalize crowded paths
                
            total_cost = current_cost + (base_cost * comfort_factor)
            
            if total_cost < costs[neighbor]:
                costs[neighbor] = total_cost
                prev_nodes[neighbor] = current_node
                heapq.heappush(heap, (total_cost, neighbor))
    
    # Reconstruct path
    if end not in prev_nodes:
        return [], float('infinity')
        
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = prev_nodes[current]
        
    return path, costs[end]

def interactive_test():
    """Interactive test mode with user preferences"""
    graph = load_graph()
    if not graph:
        print("Failed to load graph data.")
        return
    
    # Display available nodes
    print("\nAvailable Locations:")
    for node in sorted(graph['nodes'], key=lambda x: x['id']):
        print(f"{node['id']}: {node['name']}")
    
    # Get user input
    try:
        start = int(input("\nEnter START node number: "))
        end = int(input("Enter DESTINATION node number: "))
    except ValueError:
        print("Please enter valid numbers.")
        return
    
    # Validate nodes
    node_ids = [node['id'] for node in graph['nodes']]
    if start not in node_ids or end not in node_ids:
        print("Invalid node numbers entered.")
        return
    
    # Get preferences
    prefer_shade = input("Prefer shaded routes? (y/n): ").lower() == 'y'
    prefer_less_crowded = input("Prefer less crowded routes? (y/n): ").lower() == 'y'
    
    # Find path
    path, cost = comfort_dijkstra(
        graph, 
        start, 
        end,
        prefer_shade=prefer_shade,
        prefer_less_crowded=prefer_less_crowded
    )
    
    # Display results
    # Display results
    print("\n=== BEST ROUTE ===")
    if not path:
        print("No path found!")
        return
    
    print(f"Total comfort-adjusted cost: {cost:.2f}")
    print("\nRoute:")
    
    # Get all node names in order
    node_names = []
    for node_id in path:
        node = next(n for n in graph['nodes'] if n['id'] == node_id)
        node_names.append(node['name'].strip())  # Remove any extra whitespace
    
    # Print as connected path
    print(" -> ".join(node_names))
    
    # Show path statistics
    shaded_segments = 0
    uncrowded_segments = 0
    total_segments = len(path)-1
    
    if total_segments > 0:
        for i in range(len(path)-1):
            from_node = path[i]
            to_node = path[i+1]
            for edge in graph['edges']:
                if isinstance(edge, dict):
                    if (edge['from'] == from_node and edge['to'] == to_node) or \
                       (edge['from'] == to_node and edge['to'] == from_node):
                        if edge.get('has_shade', False):
                            shaded_segments += 1
                        if edge.get('less_crowd', False):
                            uncrowded_segments += 1
                        break
                else:  # list format
                    if (edge[0] == from_node and edge[1] == to_node) or \
                       (edge[0] == to_node and edge[1] == from_node):
                        if len(edge) > 4 and edge[4]:  # has_shade
                            shaded_segments += 1
                        if len(edge) > 5 and edge[5]:  # less_crowd
                            uncrowded_segments += 1
                        break
        
        print("\nPath Features:")
        print(f"- Shaded segments: {shaded_segments}/{total_segments} ({shaded_segments/total_segments:.0%})")
        print(f"- Less crowded segments: {uncrowded_segments}/{total_segments} ({uncrowded_segments/total_segments:.0%})")

if __name__ == "__main__":
    interactive_test()